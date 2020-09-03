# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class PurchaseImport(models.Model):
    _name = 'purchase.import'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Purchase import'
    _order = 'date_import desc, id desc'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    name = fields.Char('Import Reference', required=True, index=True, copy=False, default='New')
    origin = fields.Char('Source Document', copy=False)
    partner_ref = fields.Char('Reference', copy=False)
    date_import = fields.Datetime('Import Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Datetime.now)
    date_approve = fields.Datetime('Confirmation Date', readonly=1, index=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Trading', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES, default=lambda self: self.env.company.currency_id.id)
    state = fields.Selection([
        ('draft', 'draft'),
        ('purchase', 'Purchase Import'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    notes = fields.Text('Terms and Conditions')
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm', states={'done': [('readonly', True)]}, help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    user_id = fields.Many2one('res.users', string='User', index=True, tracking=True, default=lambda self: self.env.user, check_company=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)
    # currency_rate = fields.Float("Currency Rate", compute='_compute_currency_rate', compute_sudo=True, store=True, readonly=True, help='Ratio between the purchase order currency and the company currency')
    # Dates
    date_international = fields.Date(string='Port International Date', index=True)
    date_national = fields.Date(string='Port National Date', index=True)
    date_stock = fields.Date(string='Stock Date', index=True)
    # Costs
    orders_ids = fields.Many2many('purchase.order', 'import_order_rel', 'import_id', 'order_id', 'Orders', states=READONLY_STATES, copy=False)
    moves_ids = fields.Many2many('account.move', 'import_move_rel', 'import_id', 'move_id', 'Invoices', copy=False)
    # Moves
    picking_ids = fields.One2many('stock.picking', 'import_id', 'Stock Pickings', copy=False)
    move_lines = fields.One2many('stock.move', 'import_id', 'Stock Moves', copy=False)
    move_lines_done = fields.Many2many('stock.move', 'move_import_rel', 'import_id', 'move_id', 'Stock Moves Done', compute='_compute_move_lines_done')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_import' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_import']))
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.import', sequence_date=seq_date) or '/'
        return super(PurchaseImport, self).create(vals)

    def _compute_move_lines_done(self):
        for purchase in self:
            purchase.move_lines_done = purchase.move_lines.filtered(lambda m: m.state == 'done')

    def action_purchase(self):
        self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
    
    def action_progress(self):
        self._action_progress()
        self.write({'state': 'progress'})
    
    def _action_progress(self):
        for purchase in self:
            picking_ids = purchase.orders_ids.picking_ids.filtered(lambda p: p.state == 'assigned')
            move_lines = picking_ids.move_lines.filtered(lambda m: m.state == 'assigned')
            picking_ids.write({'import_id': purchase.id})
            move_lines.write({'import_id': purchase.id})

    def action_purchase_order(self):
        self.orders_ids.action_purchase_import()

    def action_validate(self):
        self.action_purchase_order()
        self.write({'state': 'done'})
        self.moves_ids.write({'import_bool': True})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def button_validate(self):
        self.ensure_one()
        if not self.move_lines:
            raise UserError(_('Please add some items to move.'))

        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.picking_ids.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in self.picking_ids.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        # If no lots when needed, raise error
        for picking in self.picking_ids:
            picking_type = picking.picking_type_id
            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            raise UserError(_('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        option = 'demand' if no_quantities_done else 'backorder'
        self._assign_percent(option)

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            vals = {
                'pick_ids': [(6, 0, self.picking_ids.ids)],
                'import_id': self.id
            }
            wiz = self.env['stock.immediate.transfer'].create(vals)
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        picking_ids = self.picking_ids
        backorder = False
        for picking in picking_ids:
            backorder = picking._check_backorder()
        if backorder:
            return picking_ids.action_generate_backorder_wizard()
        for picking in picking_ids:
            picking.action_done()
        return

    def _compute_amount_total(self):
        self.ensure_one()
        amount_total = abs(sum(move.amount_total_signed for move in self.moves_ids))
        return amount_total

    def _assign_percent(self, option):
        self.ensure_one()
        moves = self.move_lines if option == 'demand' else self.move_lines.filtered(lambda m: m.quantity_done)
        total = sum(move.price_unit * (move.product_uom_qty if option == 'demand' else move.quantity_done) for move in moves)
        for move in moves:
            percentage = (move.price_unit * (move.product_uom_qty if option == 'demand' else move.quantity_done)) / total
            move.write({'import_percentage': percentage})
