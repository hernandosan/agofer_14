# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountConsignment(models.Model):
    _name = 'account.consignment'
    _description = 'Account Consignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    amount = fields.Monetary('Amount', tracking=True)
    bank_id = fields.Many2one('res.bank', 'Bank', tracking=True)
    # branch = fields.Char('Branch')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, readonly=True)
    currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    date = fields.Date('Date', default=fields.Date.today())
    date_consignment = fields.Date('Date consignment', default=fields.Date.today())
    invoices_ids = fields.Many2many('account.move', string='Invoices', 
        domain=[('move_type', '=', 'out_invoice'),('state', 'not in', ('draft', 'cancel')),('payment_state', '!=', 'paid')])
    journal_id = fields.Many2one(related='bank_id.journal_id')
    move_id = fields.Many2one('account.move', 'Account move', readonly=True)
    name = fields.Char('Number', required=True, readonly=True, default=_('New'))
    order_id = fields.Many2one('sale.order', 'Sale order')
    partner_id = fields.Many2one('res.partner', 'Partner', tracking=True)
    reference = fields.Char('Reference', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancel')], 'State', 
        required=True, default='draft', copy=False, tracking=True)
    team_id = fields.Many2one('crm.team', 'CRM Team')
    type = fields.Selection([('normal','Payment'),('advance','Advance'),('crossover','Crossover')], 'Type consignment', 
        copy=False, default='normal')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user, readonly=True)

    @api.model
    def create(self, vals):
        vals.update(name=self.env['ir.sequence'].next_by_code('account.consignment') or _('New'))
        return super(AccountConsignment, self).create(vals)

    def action_confirm(self):
        for consignment in self:
            consignment._action_confirm()
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})
    
    def _action_confirm(self):
        self.ensure_one()
        if self.type == 'normal':
            move_id = self._action_payment()
        elif self.type == 'advance':
            move_id = self._action_advance()
        else:
            move_id = self._action_crossover()
        self.write({'move_id': move_id})
    
    def _action_payment(self):
        self.ensure_one()
        journal_id = self.journal_id
        if not journal_id:
            raise ValidationError(_("The Bank %s has not journal") % self.bank_id.id)
        partner_id = self.partner_id
        if self.type == 'crossover' and self.invoices_ids:
            account_id = self.invoices_ids.line_ids.filtered(lambda l: l.account_id.user_type_id.type == 'receivable').account_id
            if len(account_id) > 1:
                raise ValidationError(_("The invoices have different accounts receivable. \n Create a payment and reconcile"))
        else:
            account_id = partner_id.property_account_receivable_id
        vals = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': partner_id.id,
            'destination_account_id': account_id.id,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'date': self.date_consignment,
            'journal_id': journal_id.id,
        }
        payment_id = self.env['account.payment'].create(vals)
        payment_id.action_post()
        return payment_id.move_id

    def _action_advance(self):
        self.ensure_one()
        self.ensure_one()
        journal_id = self.team_id._team_advance_journal()
        account_id = self.team_id._team_advance_account()
        vals = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': self.partner_id.id,
            'destination_account_id': account_id.id,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'date': self.date_consignment,
            'journal_id': journal_id.id,
            'order_id': self.order_id.id if self.order_id else False,
        }
        payment_id = self.env['account.payment'].create(vals)
        payment_id.action_post()
        return payment_id.move_id

    def _action_crossover(self):
        self.ensure_one()
        move_id = self._action_payment()
        id = move_id.line_ids.filtered(lambda l: l.account_id.user_type_id.type == 'receivable')
        ids = self.invoices_ids.line_ids.filtered(lambda l: l.account_id.user_type_id.type == 'receivable')
        lines = id + ids
        lines.reconcile()
        return move_id
