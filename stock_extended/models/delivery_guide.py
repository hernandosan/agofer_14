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

    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

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
    driver_plate = fields.Char(related='driver_id.plate')

    guide_bool = fields.Boolean('Has Return', default=False, copy=False)
    guide_account_invoice_ids = fields.One2many('delivery.guide.line', 'guide_account_invoice_id', 'Invoices',
                                                copy=False)
    guide_account_refund_ids = fields.One2many('delivery.guide.line', 'guide_account_refund_id', 'Refunds', copy=False)
    guide_stock_invoice_ids = fields.One2many('delivery.guide.line', 'guide_stock_invoice_id', 'Invoices Moves',
                                              copy=False)
    guide_stock_refund_ids = fields.One2many('delivery.guide.line', 'guide_stock_refund_id', 'Refunds Moves',
                                             copy=False)
    guide_type = fields.Selection([('customer', 'Customer'), ('branch', 'Branch')], 'Delivery Type', copy=False,
                                  default='customer', required=True)
    guide_subtype = fields.Selection([
        ('picking', 'Picking'),
        ('repicking', 'Repicking'),
        ('standby', 'Stand By'),
        ('other', 'Other')], 'Delivery Subtype', copy=False, tracking=True)
    guide_update = fields.Boolean('Update', default=False, copy=False)

    invoices_ids = fields.Many2many('account.move', 'guide_invoice_rel', 'guide_id', 'invoice_id', 'Invoices',
                                    copy=False)
    invoices_returns_ids = fields.Many2many('account.move', 'guide_invoice_return_rel', 'guide_id', 'invoice_id',
                                            'Credit Notes', copy=False)

    moves_ids = fields.Many2many('stock.move', 'guide_move_rel', 'guide_id', 'move_id', 'Stock Moves', copy=False)

    name = fields.Char('Number', required=True, readonly=True, default='New', copy=False)

    notes = fields.Text('Terms and Conditions')

    partner_id = fields.Many2one('res.partner', 'Carrier', required=True)

    pickings_ids = fields.Many2many('stock.picking', 'guide_picking_rel', 'guide_id', 'picking_id', 'Pickings',
                                    copy=False)

    price = fields.Monetary('Price (Kg)', tracking=True, copy=False)
    price_additional = fields.Monetary('Additional Cost')
    price_standby = fields.Monetary('Stand By')
    price_total = fields.Monetary('Total Cost (Kg)', compute='_compute_price_total')

    rate_id = fields.Many2one('delivery.rate', 'Delivery Rate')
    rate_line_id = fields.Many2one('delivery.rate.line', 'Values')
    rate_tolerance = fields.Float('Tolerance (%)', related='rate_id.tolerance')

    weight_invoice = fields.Float('Delivered Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_return = fields.Float('Returned Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_move = fields.Float('Moves Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_manual = fields.Float('Manual Weight', tracking=True)
    weight_total = fields.Float('Total Weight', compute='_compute_weight', digits='Stock Weight', store=True)
    weight_adjust = fields.Float('Adjust Weight', digits='Stock Weight')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('progress', 'Progress'),
        ('delivered', 'Delivered'),
        ('checked', 'Checked'),
        ('invoiced', 'Invoiced'),
        ('cancel', 'Cancel')], 'State', default='draft', copy=False, tracking=True)

    show_update_price_kg = fields.Boolean(string='Has Price(Kg) Changed', default=False)

    @api.depends('moves_ids', 'guide_stock_invoice_ids', 'guide_stock_refund_ids', 'weight_manual')
    def _compute_weight(self):
        for guide in self:
            weight_invoice = sum(
                move.stock_weight for move in guide.guide_stock_invoice_ids if move.stock_state != 'cancel')
            weight_return = sum(
                move.stock_weight for move in guide.guide_stock_refund_ids if move.stock_state != 'cancel')
            weight_move = sum(move.weight for move in guide.moves_ids if move.state != 'cancel')
            weight_total = weight_invoice + weight_return + weight_move + guide.weight_manual
            guide.update({
                'weight_invoice': weight_invoice,
                'weight_return': weight_return,
                'weight_move': weight_move,
                'weight_total': weight_total,
            })

    @api.depends('price', 'weight_total')
    def _compute_price_total(self):
        for guide in self:
            guide.price_total = (guide.price * guide.weight_total) + guide.price_standby + guide.price_additional

    @api.onchange('rate_line_id')
    def _onchange_rate_line_id(self):
        if self.rate_line_id:
            self.price = self.rate_line_id.name

    @api.onchange('invoices_returns_ids')
    def _onchange_invoices_returns_ids(self):
        if self.invoices_returns_ids:
            self.guide_update = True

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('delivery.guide') or '/'
        return super(DeliveryGuide, self).create(vals)

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_confirm(self):
        for guide in self:
            getattr(guide, '_action_confirm_%s' % guide.guide_type)()
        self.write({'state': 'confirm'})

    def action_progress(self):
        self.invoices_ids.write({'delivery_state': 'progress'})
        self.guide_account_invoice_ids.write({'account_delivery_state': 'progress'})
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
        self.write({'state': 'cancel'})

    def action_update(self):
        for guide in self:
            guide._action_update()

    def _action_update(self):
        self.ensure_one()
        self.guide_account_refund_ids.unlink()
        self.guide_stock_refund_ids.unlink()
        self = self.with_context({'account_type': 'refund'})
        guide_account_refund_ids = self._prepare_guide_line('account')
        guide_stock_refund_ids = self._prepare_guide_line('stock')
        self.write({
            'guide_account_refund_ids': guide_account_refund_ids,
            'guide_stock_refund_ids': guide_stock_refund_ids,
            'guide_update': False,
        })

    def _action_confirm_customer(self):
        self.ensure_one()
        self.guide_account_invoice_ids.unlink()
        self.guide_stock_invoice_ids.unlink()
        self = self.with_context({'account_type': 'invoice'})
        guide_account_invoice_ids = self._prepare_guide_line('account')
        guide_stock_invoice_ids = self._prepare_guide_line('stock')
        self.write({
            'guide_account_invoice_ids': guide_account_invoice_ids,
            'guide_stock_invoice_ids': guide_stock_invoice_ids,
        })

    def _action_confirm_branch(self):
        self.ensure_one()
        ids = self.pickings_ids.move_lines.ids
        self.write({'moves_ids': [(6, 0, ids)]})

    def _prepare_guide_line(self, line_type):
        self.ensure_one()
        return getattr(self, '_prepare_guide_line_%s' % line_type)()

    def _prepare_guide_line_account(self):
        self.ensure_one()
        guide_line = []
        invoices = self.invoices_ids if self._context.get('account_type') == 'invoice' else self.invoices_returns_ids
        for invoice in invoices:
            vals = {
                'line_type': 'account_invoice',
                'account_id': invoice.id,
                'account_delivery_state': 'pending'
            }
            guide_line.append((0, 0, vals))
        return guide_line

    def _prepare_guide_line_stock(self):
        self.ensure_one()
        guide_line = []
        invoices = self.invoices_ids if self._context.get('account_type') == 'invoice' else self.invoices_returns_ids
        picking_code = 'outgoing' if self._context.get('account_type') == 'invoice' else 'incoming'
        for move in invoices.invoice_line_ids.sale_line_ids.move_ids.filtered(lambda m: m.picking_code == picking_code):
            domain = [('stock_id', '=', move.id), ('line_type', '=', 'stock_invoice'),
                      ('guide_stock_invoice_id.state', '!=', 'cancel')]
            quantity_guide = sum(l.stock_product_uom_qty for l in self.env['delivery.guide.line'].search(domain)) or 0.0
            quantity = move.product_uom_qty - quantity_guide
            vals = {
                'line_type': 'stock_invoice',
                'stock_id': move.id,
                'stock_product_uom_qty': quantity,
                'stock_product_qty': quantity
            }
            guide_line.append((0, 0, vals))
        return guide_line

    @api.onchange('weight_adjust')
    def _onchange_adjust_weight(self):
        if self.weight_adjust != self.weight_adjust:
            self.show_update_price_kg = False
        else:
            self.show_update_price_kg = True

    def update_prices(self):
        self.update({'price': ((self.rate_line_id.name * self.weight_adjust)/self.weight_total)})
        self.show_update_price_kg = False
        self.message_post(body=_("Price(Kg) have been recomputed according to pricelist <b>%s<b>", self.weight_adjust))


class DeliveryGuideLine(models.Model):
    _name = 'delivery.guide.line'
    _description = 'Delivery Guide Line'
    _rec_name = 'line_type'

    # Account
    account_amount_total_signed = fields.Monetary(related='account_id.amount_total_signed')
    account_delivery_bool = fields.Boolean('Has Novelty', default=False)
    account_delivery_state = fields.Selection([
        ('pending', 'Pending'),
        ('progress', 'Progress'),
        ('delivered', 'Delivered')
    ], 'Delivery State')
    account_id = fields.Many2one('account.move', 'Invoice')
    account_date = fields.Date(related='account_id.invoice_date')
    account_name = fields.Char(related='account_id.name')
    account_order_id = fields.Many2one(related='account_id.order_id')
    account_partner_id = fields.Many2one(related='account_id.partner_id')
    account_state = fields.Selection(related='account_id.state')

    # Company
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(related='company_id.currency_id')

    # Guide
    guide_account_invoice_id = fields.Many2one('delivery.guide', 'Guide Invoice')
    guide_account_refund_id = fields.Many2one('delivery.guide', 'Guide Refund')
    guide_stock_invoice_id = fields.Many2one('delivery.guide', 'Guide Invoice Move')
    guide_stock_refund_id = fields.Many2one('delivery.guide', 'Guide Refund Move')

    # Line
    line_type = fields.Selection([
        ('account_invoice', 'Invoice'),
        ('account_refund', 'Refund'),
        ('stock_invoice', 'Invoice Move'),
        ('stock_refund', 'Refund Move'),
    ], 'Type', required=True, default='')

    # Move
    stock_date = fields.Datetime(related='stock_id.date')
    stock_id = fields.Many2one('stock.move', 'Invoice Move')
    stock_picking_id = fields.Many2one(related='stock_id.picking_id')
    stock_product_id = fields.Many2one(related='stock_id.product_id')
    stock_product_uom_qty = fields.Float('Demand', digits='Product Unit of Measure')
    stock_product_qty = fields.Float('Quantity', digits='Product Unit of Measure')
    stock_state = fields.Selection(related='stock_id.state')
    stock_uom_id = fields.Many2one(related='stock_product_id.uom_id')
    stock_weight = fields.Float(compute='_compute_stock_weight', digits='Weight', store=True)

    @api.onchange('stock_product_qty')
    def _onchange_stock_product_qty(self):
        if self.stock_product_qty > self.stock_product_uom_qty:
            raise ValidationError(_("The quantity cannot be greater than the delivered"))

    @api.depends('stock_product_id', 'stock_product_uom_qty')
    def _compute_stock_weight(self):
        moves_with_weight = self.filtered(lambda moves: moves.stock_product_id.weight > 0.00)
        for move in moves_with_weight:
            move.stock_weight = (move.stock_product_uom_qty * move.stock_product_id.weight)
        (self - moves_with_weight).stock_weight = 0

    def action_confirm(self):
        for line in self:
            line._action_confirm()

    def _action_confirm(self):
        self.ensure_one()
        vals = {'account_delivery_state': 'delivered'}
        domain = [('account_id', '=', self.account_id.id), ('line_type', '=', 'account_invoice'),
                  ('guide_account_invoice_id.state', '!=', 'cancel')]
        if self._context.get('guide_refund'):
            domain = [('account_id', '=', self.account_id.id), ('line_type', '=', 'account_refund'),
                      ('guide_account_refund_id.state', '!=', 'cancel')]
        lines = self.env['delivery.guide.line'].search(domain)
        vals_invoice = {'delivery_state': 'delivered'}
        if len(lines) > 1:
            vals_invoice.update(delivery_state='partial')
        self.account_id.write(vals_invoice)
        if self._context.get('guide_return'):
            vals.update(account_delivery_bool=True)
            if not self.guide_account_refund_id.guide_bool:
                self.guide_account_refund_id.write({'guide_bool': True})
        self.update(vals)
