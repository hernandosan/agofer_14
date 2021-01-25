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
    carrier_tolerance = fields.Float('Tolerance (%)', related='carrier_id.tolerance')

    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True, default=lambda self: self.env.company)

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)

    date_progress = fields.Date('Progress Date')
    date_delivered = fields.Date('Delivered Date')
    date_checked = fields.Date('Checked Date')
    date_invoiced = fields.Date('Invoiced Date')
    date_scheduled = fields.Date('Scheduled Date', required=True, default=fields.Date.today())

    driver_comment = fields.Text(related='driver_id.comment')
    driver_id = fields.Many2one('res.partner', 'Driver')
    driver_mobile = fields.Char(related='driver_id.mobile')
    driver_name = fields.Char(related='driver_id.name')

    guide_bool = fields.Boolean('Has Return', default=False, copy=False)
    guide_invoice_id = fields.One2many('delivery.guide.move', 'guide_id', 'Moves', domain="[('move_type','=','invoice')]", copy=False)
    guide_refund_id = fields.One2many('delivery.guide.move', 'guide_id', 'Refunds', domain="[('move_type','=','refund')]", copy=False)
    guide_type = fields.Selection([('customer','Customer'),('branch','Branch')], 'Delivery Type', copy=False, default='customer')

    invoices_ids = fields.Many2many('account.move', 'guide_invoice_rel', 'guide_id', 'invoice_id', 'Invoices', copy=False)
    invoices_returns_ids = fields.Many2many('account.move', 'guide_invoice_return_rel', 'guide_id', 'invoice_id', 'Credit Notes', copy=False)

    moves_ids = fields.Many2many('stock.move', 'guide_move_rel', 'guide_id', 'move_id', 'Stock Moves', copy=False)

    name = fields.Char('Number', required=True, readonly=True, default='New', copy=False)    

    notes = fields.Text('Terms and Conditions')

    partner_id = fields.Many2one('res.partner', 'Carrier', required=True)

    pickings_ids = fields.Many2many('stock.picking', 'guide_picking_rel', 'guide_id', 'picking_id', 'Pickings', copy=False)

    price = fields.Monetary('Price (Kg)', tracking=True, copy=False)
    price_kg = fields.Monetary('Carrier Price')
    price_standby = fields.Monetary('Stand By')
    price_total = fields.Monetary('Total Cost (Kg)', compute='_compute_price_total')

    weight_invoice = fields.Float('Delivered Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_return = fields.Float('Returned Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_move = fields.Float('Moves Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_total = fields.Float('Total Weight', compute='_compute_weight', digits='Stock Weight', store=True)

    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('progress','Progress'),
        ('delivered','Delivered'),
        ('checked','Checked'),
        ('invoiced','Invoiced'),
        ('cancel','Cancel')], 'State', default='draft', copy=False, tracking=True)

    @api.depends('moves_ids', 'guide_invoice_id', 'guide_refund_id', 'moves_ids')
    def _compute_weight(self):
        for guide in self:
            weight_invoice = sum(move.weight for move in guide.guide_invoice_id if move.move_state != 'cancel')
            weight_return = sum(move.weight for move in guide.guide_refund_id if move.move_state != 'cancel')
            weight_move = sum(move.weight for move in guide.moves_ids if move.state != 'cancel')
            weight_total = weight_invoice + weight_return + weight_move
            guide.update({
                'weight_invoice': weight_invoice,
                'weight_return': weight_return,
                'weight_move': weight_move,
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

    @api.onchange('price')
    def _onchange_price(self):
        if self.price and ((self.price - self.price_kg) / self.price_kg) * 100 > self.carrier_tolerance and not self.user.has_group('stock.group_stock_manager'):
            raise ValidationError(_("The price exceeds the allowed tolerance"))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.guide') or '/'
        return super(DeliveryGuide, self).create(vals)

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_confirm(self):
        for guide in self.filtered(lambda s: s.guide_type == 'customer'):
            guide._action_confirm_customer()
        for guide in self.filtered(lambda s: s.guide_type == 'branch'):
            guide._action_confirm_branch()
        self.write({'state': 'confirm'})

    def _action_confirm_customer(self):
        self.ensure_one()
        guide_invoice_id = self._prepare_guide_invoice()
        self.write({'guide_invoice_id': guide_invoice_id})

    def _action_confirm_branch(self):
        self.ensure_one()
        ids = self.pickings_ids.move_lines.ids
        self.write({'moves_ids': [(6, 0, ids)]})

    def _prepare_guide_invoice(self, move_type='invoice'):
        self.ensure_one()
        guide_invoice = []
        invoices = self.invoices_ids if move_type == 'invoice' else self.invoices_returns_ids
        picking_code = 'outgoing' if move_type == 'invoice' else 'incoming'
        for move in invoices.invoice_line_ids.sale_line_ids.move_ids.filtered(lambda m: m.picking_code == picking_code):
            domain = [('move_id','=',move.id),('move_state','!=','cancel')]
            quantity_guide = sum(g.product_uom_qty for g in self.env['delivery.guide.move'].search(domain)) or 0.0
            quantity = move.product_uom_qty - quantity_guide
            vals = {
                'move_id': move.id,
                'move_type': move_type,
                'product_uom_qty': quantity,
                'guide_qty': quantity
            }
            if quantity > 0:
                guide_invoice.append((0,0,vals))
        return guide_invoice

    def action_moves(self):
        for guide in self:
            guide._action_moves()

    def _action_moves(self):
        self.ensure_one()
        guide_refund_id = self._prepare_guide_invoice(move_type='refund')
        self.write({'guide_refund_id': guide_refund_id})

    def action_progress(self):
        self.invoices_ids.write({'delivery_state': 'progress'})
        self.write({
            'state': 'progress',
            'date_progress': fields.Date.today(),
        })

    def action_delivered(self):
        self.write({
            'state': 'delivered',
            'date_delivered': fields.Date.today(),
        })

    def action_checked(self):
        self.write({
            'state': 'checked',
            'date_checked': fields.Date.today()})

    def action_invoiced(self):
        self.write({
            'state': 'invoiced',
            'date_invoiced': fields.Date.today(),
        })

    def action_cancel(self):
        self.invoices_ids.write({'delivery_state': 'pending'})
        self.invoices_returns_ids.write({'delivery_state': 'pending'})
        self.write({'state': 'cancel'})


class DeliveryGuideMove(models.Model):
    _name = 'delivery.guide.move'
    _description = 'Delivery Guide Move'
    _rec_name = 'move_id'

    guide_id = fields.Many2one('delivery.guide', 'Guide', ondelete='cascade', required=True)
    guide_qty = fields.Float('Guide Quantity', digits='Product Unit of Measure')
    move_id = fields.Many2one('stock.move', 'Move', ondelete='restrict', required=True)
    move_state = fields.Selection(related='move_id.state')
    move_type = fields.Selection([('invoice','Invoice'),('refund','Refund')], 'Type', default='invoice')
    picking_id = fields.Many2one(related='move_id.picking_id')
    product_id = fields.Many2one(related='move_id.product_id')
    product_uom_id = fields.Many2one(related='product_id.uom_id')
    product_uom_qty = fields.Float('Quantity', digits='Product Unit of Measure')
    weight = fields.Float(compute='_compute_weight', digits='Weight', store=True)

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        if self.product_uom_qty > self.guide_qty:
            raise ValidationError(_("The quantity cannot be greater than the delivered"))

    @api.depends('product_id', 'product_uom_qty')
    def _compute_weight(self):
        moves_with_weight = self.filtered(lambda moves: moves.product_id.weight > 0.00)
        for move in moves_with_weight:
            move.weight = (move.product_uom_qty * move.product_id.weight)
        (self - moves_with_weight).weight = 0
