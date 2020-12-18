# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DeliveryGuide(models.Model):
    _name = 'delivery.guide'
    _description = 'Delivery Guide'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    analytic_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    carrier_id = fields.Many2one('delivery.carrier', 'Tariff', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    date_progress = fields.Date('Progress Date')
    date_delivered = fields.Date('Delivered Date')
    date_checked = fields.Date('Checked Date')
    date_invoiced = fields.Date('Invoiced Date')
    driver_comment = fields.Text(related='partner_id.comment')
    driver_id = fields.Many2one('res.partner', 'Driver')
    driver_mobile = fields.Char(related='partner_id.mobile')
    driver_name = fields.Char(related='partner_id.name')
    guide_bool = fields.Boolean('Has Return', default=False, copy=False)
    guide_type = fields.Selection([('customer','Customer'),('branch','Branch')], 'Delivery Type', copy=False, default='customer')
    invoices_ids = fields.Many2many('account.move', 'guide_invoice_rel', 'guide_id', 'invoice_id', 'Invoices', copy=False)
    invoices_returns_ids = fields.Many2many('account.move', 'guide_invoice_return_rel', 'guide_id', 'invoice_id', 'Credit Notes', copy=False)
    moves_ids = fields.Many2many('stock.move', 'guide_move_rel', 'guide_id', 'move_id', 'Stock Moves', copy=False)
    moves_returns_ids = fields.Many2many('stock.move', 'guide_move_return_rel', 'guide_id', 'move_id', 'Stock Moves Return', copy=False)
    name = fields.Char('Number', required=True, readonly=True, default='New', copy=False)    
    notes = fields.Text('Terms and Conditions')
    partner_id = fields.Many2one('res.partner', 'Carrier', required=True)
    pickings_ids = fields.Many2many('stock.picking', 'guide_picking_rel', 'guide_id', 'picking_id', 'Pickings', copy=False)
    price = fields.Monetary('Price (Kg)', tracking=True, copy=False)
    price_kg = fields.Monetary('Carrier Price')
    price_standby = fields.Monetary('Stand By')
    price_total = fields.Monetary('Total Cost (Kg)', compute='_compute_price_total')
    scheduled_date = fields.Date('Scheduled Date', required=True)
    tolerance = fields.Float('Tolerance (%)', copy=False)
    weight_invoice = fields.Float('Delivered Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_return = fields.Float('Returned Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_total = fields.Float('Total Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('progress','Progress'),
        ('delivered','Delivered'),
        ('checked','Checked'),
        ('invoiced','Invoiced'),
        ('cancel','Cancel')], 'State', default='draft', copy=False, tracking=True)

    @api.depends('moves_ids', 'moves_returns_ids')
    def _compute_weight(self):
        for guide in self:
            weight_invoice = sum(move.weight for move in guide.moves_ids if move.state != 'cancel')
            weight_return = sum(move.weight for move in guide.moves_returns_ids if move.state != 'cancel')
            weight_total = weight_invoice + weight_return
            guide.update({
                'weight_invoice': weight_invoice,
                'weight_return': weight_return,
                'weight_total': weight_total,
            })

    @api.depends('price', 'weight_total')
    def _compute_price_total(self):
        for guide in self:
            guide.price_total = (guide.price * guide.weight_total) + guide.price_standby

    @api.onchange('carrier_id')
    def _onchange_carrier_id(self):
        if self.carrier_id:
            self.price_kg = self.carrier_id.price_kg
            self.price = self.carrier_id.price_kg
            self.tolerance = self.carrier_id.tolerance

    @api.onchange('price')
    def _onchange_price(self):
        if self.price and ((self.price - self.price_kg) / self.price_kg) * 100 > self.tolerance and not self.user.has_group('stock.group_stock_manager'):
            raise ValidationError(_("The price exceeds the allowed tolerance"))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.guide') or '/'
        return super(DeliveryGuide, self).create(vals)

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_confirm(self):
        for guide in self:
            guide._action_confirm()
        self.write({'state': 'confirm'})

    def _action_confirm(self):
        self.ensure_one()
        ids = self.invoices_ids.picking_id.move_lines.ids if self.guide_type == 'customer' else self.pickings_ids.move_lines.ids
        self.write({'moves_ids': [(6, 0, ids)]})

    def action_moves(self):
        for guide in self:
            guide._action_moves()

    def _action_moves(self):
        self.ensure_one()
        self.write({'moves_ids': [(6, 0, self.invoices_ids.picking_id.move_lines.ids)]})
        self.write({'moves_returns_ids': [(6, 0, self.invoices_returns_ids.picking_id.move_lines.ids)]})

    def action_progress(self):
        self.invoices_ids.write({'delivery_state': 'progress'})
        self.write({
            'state': 'progress',
            'progress_date': fields.Date.today(),
        })

    def action_delivered(self):
        self._action_delivered()
        self.write({
            'state': 'delivered',
            'delivered_date': fields.Date.today(),
        })

    def _action_delivered(self):
        self.ensure_one()
        # self.invoices_ids.write({'delivery_state': 'delivered'})
        self.write({'moves_returns_ids': [(6, 0, self.invoices_returns_ids.picking_id.move_lines.ids)]})

    def action_checked(self):
        self.write({
            'state': 'checked',
            'checked_date': fields.Date.today()})

    def action_invoiced(self):
        self.write({
            'state': 'invoiced',
            'invoiced_date': fields.Date.today(),
        })

    def action_cancel(self):
        self.invoices_ids.write({'delivery_state': 'pending'})
        self.invoices_returns_ids.write({'delivery_state': 'pending'})
        self.write({'state': 'cancel'})
