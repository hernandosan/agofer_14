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
    move_lines_done = fields.One2many('stock.move', 'import_done_id', 'Stock Moves Done', copy=False)
    moves_lines = fields.Many2many('stock.move', 'move_import_rel', 'import_id', 'move_id', 'Stocks Moves', compute='_compute_move_lines_done')
    # Totals
    import_line = fields.One2many('purchase.import.line', 'import_id', string='Import Lines', copy=False)
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    invoice_tariff = fields.Many2one('account.move', 'Invoice Tariff', copy=False)
    invoice_vat = fields.Many2one('account.move', 'Invoice Vat', copy=False)
    # Taxes
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

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
            purchase.moves_lines = purchase.move_lines_done.filtered(lambda m: m.state == 'done')

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

    def action_stock_move(self):
        for purchase in self:
            purchase.move_lines.write({'import_done_id': purchase.id})

    def action_validate(self):
        self.action_purchase_order()
        self.action_stock_move()
        self.moves_ids.write({'import_bool': True})
        self.picking_ids.write({'import_id': False})
        self.move_lines.write({'import_id': False})
        self.write({'state': 'done'})

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
        self._action_validate(option)

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

    def _compute_amount_total(self, option):
        # option: tariff, vat
        self.ensure_one()
        moves = self.moves_ids.filtered(lambda m: m.import_type != 'tariff') if option == 'tariff' else self.moves_ids.filtered(lambda m: m.import_type != 'vat')
        amount_total = abs(sum(move.amount_total_signed for move in moves))
        return amount_total

    def _assign_percent(self, option):
        self.ensure_one()
        moves = self.move_lines if option == 'demand' else self.move_lines.filtered(lambda m: m.quantity_done)
        total = sum(move.price_unit * (move.product_uom_qty if option == 'demand' else move.quantity_done) for move in moves)
        for move in moves:
            percentage = (move.price_unit * (move.product_uom_qty if option == 'demand' else move.quantity_done)) / total
            move.write({'import_percentage': percentage})

    def _action_validate(self, option):
        self.ensure_one()
        # Create tariff invoice
        moves = self.move_lines if option == 'demand' else self.move_lines.filtered(lambda m: m.quantity_done)
        self._action_create_line(moves, option)
        self._action_create_invoice('tariff')

    # Lines
    @api.depends('import_line.price_total')
    def _amount_all(self):
        for purchase in self:
            amount_untaxed = amount_tax = 0.0
            for line in purchase.import_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            purchase.update({
                'amount_untaxed': purchase.currency_id.round(amount_untaxed),
                'amount_tax': purchase.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    def _action_create_line(self, moves, option):
        self.ensure_one()
        self.import_line.sudo().unlink()
        import_line = []
        amount_total = self._compute_amount_total('tariff')
        for move in moves:
            price_unit = move._get_price_unit_purchase() or move._get_price_unit()
            price_customs = price_unit + (move.import_percentage * amount_total)
            vals = {
                'product_id': move.product_id.id,
                'name': move.product_id.display_name,
                'product_qty': move.product_uom_qty if option == 'demand' else move.quantity_done,
                'product_uom': move.product_uom.id,
                'price_unit': price_unit,
                'price_customs': price_customs,
                'taxes_tariff_id': [(4, t.id) for t in move.product_id.tariff_ids.filtered(lambda t: t.country_id == self.partner_id.country_id).tax_id]
            }
            import_line.append((0, 0, vals))
        self.write({'import_line': import_line})

    def _action_create_invoice(self, option):
        self.ensure_one()
        self._check_invoice(option)
        invoice_line_ids = []
        lines = self.import_line.filtered(lambda l: l.taxes_tariff_id) if option == 'tariff' else self.import_line.filtered(lambda l: l.taxes_id)
        for line in lines:
            taxes = line.taxes_tariff_id if option == 'tariff' else line.taxes_id
            for tax in taxes:
                compute_all = tax.compute_all(line.price_customs, self.currency_id, quantity=line.product_qty, product=line.product_id, partner=line.partner_id)
                dics = compute_all.get('taxes')
                for dic in dics:
                    val = {
                        'name': '[' + self.name + '] ' + dic.get('name'),
                        'account_id': dic.get('account_id'),
                        'price_unit': dic.get('amount'),
                        'tax_ids': False,
                    }
                    invoice_line_ids.append((0,0,val))
        if invoice_line_ids:
            vals = {
                'type': 'in_invoice',
                'company_id': self.company_id.id,
                'invoice_origin': self.name,
                'import_id': self.id,
                'import_type': 'tariff',
                'invoice_line_ids': invoice_line_ids
            }
            invoice = self.invoice_tariff if option == 'tariff' else self.invoice_vat
            if invoice:
                invoice.write(vals)
            else:
                am_id = self.env['account.move'].sudo().create(vals)
                am = {'invoice_tariff': am_id.id} if option == 'tariff' else {'invoice_vat': am_id.id}
                self.write(am)

    def _check_invoice(self, option):
        self.ensure_one()
        invoice = self.invoice_tariff if option == 'tariff' else self.invoice_vat
        if invoice and invoice.state == 'posted':
            invoice.button_draft()


class PurchaseImportLine(models.Model):
    _name = 'purchase.import.line'
    _description = 'Purchase Import Line'
    _order = 'import_id, sequence, id'

    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True)
    product_uom_qty = fields.Float(string='Total Quantity', compute='_compute_product_uom_qty', store=True)
    date_planned = fields.Datetime(string='Scheduled Date', index=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes')
    taxes_tariff_id = fields.Many2many('account.tax', 'tax_import_res', string='Taxes tariff')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    product_type = fields.Selection(related='product_id.type', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)
    price_tax_tariff = fields.Float(compute='_compute_amount_tariff', string='Tax Tariff', store=True)

    import_id = fields.Many2one('purchase.import', string='Import Reference', index=True, required=True, ondelete='cascade')
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    company_id = fields.Many2one('res.company', related='import_id.company_id', string='Company', store=True, readonly=True)
    state = fields.Selection(related='import_id.state', store=True, readonly=False)

    invoice_lines = fields.One2many('account.move.line', 'purchase_line_id', string="Bill Lines", readonly=True, copy=False)

    partner_id = fields.Many2one('res.partner', related='import_id.partner_id', string='Partner', readonly=True, store=True)
    currency_id = fields.Many2one(related='import_id.currency_id', store=True, string='Currency', readonly=True)
    date_order = fields.Datetime(related='import_id.date_import', string='Order Date', readonly=True)

    qty_invoiced = fields.Float(compute='_compute_qty_invoiced', string="Billed Qty", digits='Product Unit of Measure', store=True)

    qty_received_method = fields.Selection([('manual', 'Manual')], string="Received Qty Method", compute='_compute_qty_received_method', store=True,
        help="According to product configuration, the recieved quantity can be automatically computed by mechanism :\n"
             "  - Manual: the quantity is set manually on the line\n"
             "  - Stock Moves: the quantity comes from confirmed pickings\n")
    qty_received = fields.Float("Received Qty", compute='_compute_qty_received', inverse='_inverse_qty_received', compute_sudo=True, store=True, digits='Product Unit of Measure')
    qty_received_manual = fields.Float("Manual Received Qty", digits='Product Unit of Measure', copy=False)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    
    # Costs
    price_customs = fields.Float('Customs Price', digits='Product Price')
    price_tariff = fields.Float('Tariff Price', digits='Product Price')
    price_vat = fields.Float('Vat Price', digits='Product Price')
    base_vat = fields.Float('Base VAT', digits='Product Price')

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('product_qty', 'price_customs', 'taxes_tariff_id')
    def _compute_amount_tariff(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_tariff_id.compute_all(
                vals['price_customs'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax_tariff': sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
            })

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        return {
            'price_unit': self.price_unit,
            'price_customs': self.price_customs,
            'currency_id': self.import_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            'partner': self.import_id.partner_id,
        }

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
    def _compute_qty_invoiced(self):
        for line in self:
            qty = 0.0
            for inv_line in line.invoice_lines:
                if inv_line.move_id.state not in ['cancel']:
                    if inv_line.move_id.type == 'in_invoice':
                        qty += inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
                    elif inv_line.move_id.type == 'in_refund':
                        qty -= inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
            line.qty_invoiced = qty
