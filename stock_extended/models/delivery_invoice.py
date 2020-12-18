# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DeliveryInvoice(models.Model):
    _name = 'delivery.invoice'
    _description = 'Delivery Invoice'
    _order = 'id desc'
    _rec_name = 'move_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    guides_ids = fields.Many2many('delivery.guide', string='Guides')
    journal_id = fields.Many2one('account.journal', 'Journal')
    move_id = fields.Many2one('account.move', 'Invoice')
    notes = fields.Text('Notes')
    partner_id = fields.Many2one('res.partner', 'Carrier')
    price_total = fields.Monetary('Total Price', compute='_compute_price_total')
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Cancel')], 'state', required=True, default='draft')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    weight_invoiced = fields.Float('Weight', compute='_compute_weight')
    weight_returned = fields.Float('Weight Returned', compute='_compute_weight')

    @api.depends('guides_ids')
    def _compute_price_total(self):
        for invoice in self:
            invoice.price_total = sum(guide.price_total for guide in invoice.guides_ids)

    @api.depends('guides_ids')
    def _compute_weight(self):
        for invoice in self:
            invoice.weight_invoiced = sum(guide.weight_invoice for guide in invoice.guides_ids)
            invoice.weight_returned = sum(guide.weight_return for guide in invoice.guides_ids)

    def action_confirm(self):
        for invoice in self:
            invoice._action_confirm()
        self.write({'state': 'done'})
    
    def _action_confirm(self):
        self.ensure_one()
        if not self.guides_ids:
            raise ValidationError(_('Please add guides'))
        move_id = self.env['account.move'].create(self._prepare_account_move())
        self.guides_ids.write({'state': 'invoiced'})
        self.write({'move_id': move_id.id})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def _prepare_account_move(self):
        self.ensure_one()
        invoice_line_ids = self._prepare_account_move_line()
        vals = {
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'journal_id': self.journal_id.id,
            'invoice_line_ids': invoice_line_ids,
            'narration': self.notes,
        }
        return vals

    def _prepare_account_move_line(self):
        self.ensure_one()
        lines = []
        for guide in self.guides_ids:
            product_id = guide.carrier_id.product_id
            accounts = product_id._get_product_accounts()
            vals = {
                'product_id': product_id.id,
                'product_uom_id': product_id.uon_id.id,
                'name': product_id.display_name,
                'account_id': accounts.get('expense'),
                'analytic_account_id': guide.analytic_account_id.id,
                'analytic_tag_ids': [(4, tag.id, 0) for tag in guide.analytic_tag_ids],
                'quantity': guide.weight_total,
                'price_unit': guide.price,
            }
            lines.append((0,0,vals))
        return lines
