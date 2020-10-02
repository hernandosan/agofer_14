# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DeliveryGuide(models.Model):
    _name = 'delivery.guide'
    _description = 'Delivery Guide'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    name = fields.Char('Number', required=True, readonly=True, default='New', copy=False)
    delivery_type = fields.Selection([('customer','Customer'),('branch','Branch')], 'Delivery Type', copy=False, default='customer')
    parent_id = fields.Many2one('res.partner', 'Carrier', required=True)
    partner_id = fields.Many2one('res.partner', 'Driver')
    carrier_id = fields.Many2one('delivery.carrier', 'Tariff', required=True)
    tolerance = fields.Float('Tolerance (%)', copy=False)
    analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    scheduled_date = fields.Date('Scheduled Date', required=True)
    progress_date = fields.Date('Progress Date')
    delivered_date = fields.Date('Delivered Date')
    done_date = fields.Date('Done Date')
    invoiced_date = fields.Date('Invoiced Date')
    price_kg = fields.Monetary('Carrier Price')
    price = fields.Monetary('Price (Kg)')
    weight = fields.Float('Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    # weight = fields.Float('Weight', digits='Stock Weight')
    price_total = fields.Monetary('Total Cost (Kg)', compute='_compute_price_total')
    notes = fields.Text('Terms and Conditions')
    invoices_ids = fields.Many2many('account.move', 'guide_invoice_rel', 'guide_id', 'invoice_id', 'Invoices')
    moves_ids = fields.Many2many('stock.move', 'guide_move_rel', 'guide_id', 'move_id', 'Stock Moves')
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('progress','Progress'),
        ('delivered','Delivered'),
        ('done','Done'),
        ('invoiced','Invoiced'),
        ('cancel','Cancel')], 'State', default='draft', copy=False, tracking=True)

    @api.depends('moves_ids')
    def _compute_weight(self):
        for guide in self:
            guide.weight = sum(move.weight for move in guide.moves_ids if move.state != 'cancel')

    @api.depends('price', 'weight')
    def _compute_price_total(self):
        for guide in self:
            guide.price_total = guide.price * guide.weight

    @api.onchange('carrier_id')
    def _onchange_carrier_id(self):
        if self.carrier_id:
            self.price_kg = self.carrier_id.price_kg
            self.price = self.carrier_id.price_kg
            self.tolerance = self.carrier_id.tolerance

    @api.onchange('price')
    def _onchange_price(self):
        if self.price and ((self.price - self.price_kg) / self.price_kg) * 100 > self.tolerance:
            raise ValidationError(_("The price exceeds the allowed tolerance"))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.guide') or '/'
        return super(DeliveryGuide, self).create(vals)

    def action_confirm(self):
        self._action_confirm()
        self.write({'state': 'confirm'})

    def _action_confirm(self):
        self.ensure_one()
        self.write({'moves_ids': [(6, 0, self.invoices_ids.picking_id.ids)]})

    def action_progress(self):
        self.invoices_ids.write({'delivery_state': 'progress'})
        self.write({
            'state': 'progress',
            'progress_date': fields.Date.today(),
        })

    def action_delivered(self):
        self.write({
            'state': 'delivered',
            'delivered_date': fields.Date.today(),
        })

    def action_done(self):
        self.write({
            'state': 'done',
            'done_date': fields.Date.today(),
        })

    def action_invoiced(self):
        self.write({
            'state': 'invoiced',
            'invoiced_date': fields.Date.today(),
        })

    def action_cancel(self):
        self.write({'state': 'cancel'})
