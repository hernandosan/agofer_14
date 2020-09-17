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

    name = fields.Char('Number', required=True, index=True, copy=False, default='New')
    origin = fields.Char('Source Document', copy=False)
    partner_ref = fields.Char('Reference', copy=False)
    partner_id = fields.Many2one('res.partner', string='Trading', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    currency_company_id = fields.Many2one(related='company_id.currency_id', store=True, string='Currency Company', readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES, default=lambda self: self.env.company.currency_id.id)
    currency_rate = fields.Float("Currency Rate", compute='_compute_currency_rate', compute_sudo=True, store=True, readonly=True, help='Ratio between the purchase order currency and the company currency')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('purchase', 'Purchase Import'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    notes = fields.Text('Terms and Conditions')
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm', states={'done': [('readonly', True)]}, help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    user_id = fields.Many2one('res.users', string='User', index=True, tracking=True, default=lambda self: self.env.user, check_company=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)
    # Dates
    date_import = fields.Datetime('Import Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Datetime.now)
    date_approve = fields.Datetime('Confirmation Date', readonly=1, index=True, copy=False)
    date_international = fields.Date(string='Port International Date', index=True)
    date_national = fields.Date(string='Port National Date', index=True)
    date_stock = fields.Date(string='Stock Date', index=True)
    # Costs
    price_type = fields.Selection([('price','Price'), ('weight','Weight')], 'Price Type', copy=False, default='price')
    orders_ids = fields.Many2many('purchase.order', 'import_order_rel', 'import_id', 'order_id', 'Orders', states=READONLY_STATES, copy=False)
    moves_ids = fields.Many2many('account.move', 'import_move_rel', 'import_id', 'move_id', 'Invoices', copy=False)
    # Moves
    picking_ids = fields.One2many('stock.picking', 'import_id', 'Stock Pickings', copy=False)
    move_lines = fields.One2many('stock.move', 'import_id', 'Stock Moves', copy=False)
    move_lines_done = fields.One2many('stock.move', 'import_done_id', 'Stock Moves Done', copy=False)
    # Totals
    import_line = fields.One2many('purchase.import.line', 'import_id', string='Import Lines', copy=False)
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    # Amount
    amount_cost = fields.Monetary('Cost Amount Local', currency_field='currency_company_id')
    amount_cost_currency = fields.Monetary('Cost Amount', compute='_compute_amount', store=True)
    amount_insurance = fields.Monetary('Insurance Amount Local', currency_field='currency_company_id', compute='_compute_amount', store=True)
    amount_insurance_currency = fields.Monetary('Insurance Amount')
    amount_freight = fields.Monetary('Freight Amount Local', currency_field='currency_company_id', compute='_compute_amount', store=True)
    amount_freight_currency = fields.Monetary('Freight Amount')
    amount_cif = fields.Monetary('CIF Amount', currency_field='currency_company_id', compute='_compute_amount', store=True)

    amount_expense = fields.Monetary('Expense Amount', store=True, readonly=True, compute='_compute_expense', currency_field='currency_company_id')
    amount_tariff = fields.Monetary('Tariff Amount', store=True, readonly=True, compute='_compute_amount_line', currency_field='currency_company_id')
    amount_vat = fields.Monetary('VAT Amount', store=True, readonly=True, compute='_compute_amount_line', currency_field='currency_company_id')

    amount_tax = fields.Monetary('Taxes', store=True, readonly=True, compute='_amount_all', currency_field='currency_company_id')
    amount_untaxed = fields.Monetary('Untaxed Amount', store=True, readonly=True, compute='_amount_all', currency_field='currency_company_id')
    amount_total = fields.Monetary('Total', store=True, readonly=True, compute='_amount_all', currency_field='currency_company_id')
    # Expenses
    expense_cost = fields.Monetary('Cost Expense', store=True, readonly=True, compute='_compute_expense', currency_field='currency_company_id')
    expense_insurance = fields.Monetary('Insurance Expense', store=True, readonly=True, compute='_compute_expense', currency_field='currency_company_id')
    expense_freight = fields.Monetary('Freight Expense', store=True, readonly=True, compute='_compute_expense', currency_field='currency_company_id')
    expense_other = fields.Monetary('Other Expense', store=True, readonly=True, compute='_compute_expense', currency_field='currency_company_id')
    # Invoice
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

    @api.depends('date_import', 'currency_id', 'company_id', 'company_id.currency_id')
    def _compute_currency_rate(self):
        for purchase in self:
            purchase.currency_rate = self.env['res.currency']._get_conversion_rate(purchase.company_id.currency_id, purchase.currency_id, purchase.company_id, purchase.date_import)

    @api.depends('amount_cost', 'amount_insurance_currency', 'amount_freight_currency')
    def _compute_amount(self):
        for purchase in self:
            currency_company_id = purchase.currency_company_id
            currency_id = purchase.currency_id
            amount_cost_currency = currency_company_id.with_context(date=purchase.date_import).compute(purchase.amount_cost, currency_id)
            amount_insurance = currency_id.with_context(date=purchase.date_import).compute(purchase.amount_insurance_currency, currency_company_id)
            amount_freight = currency_id.with_context(date=purchase.date_import).compute(purchase.amount_freight_currency, currency_company_id)
            amount_cif = purchase.amount_cost + amount_insurance + amount_freight
            purchase.update({
                'amount_cost_currency': amount_cost_currency,
                'amount_insurance': amount_insurance,
                'amount_freight': amount_freight,
                'amount_cif': amount_cif,
            })

    @api.depends('moves_ids.amount_total_signed')
    def _compute_expense(self):
        for purchase in self:
            expense_cost = abs(sum(move.amount_total_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'cost')))
            expense_insurance = abs(sum(move.amount_total_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'insurance')))
            expense_freight = abs(sum(move.amount_total_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'freight')))
            expense_other = abs(sum(move.amount_total_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'other')))
            amount_expense = expense_cost + expense_insurance + expense_freight + expense_other
            purchase.update({
                'expense_cost': expense_cost,
                'expense_insurance': expense_insurance,
                'expense_freight': expense_freight,
                'expense_other': expense_other,
                'amount_expense': amount_expense
                })

    @api.depends('import_line.price_tariff','import_line.price_tax')
    def _compute_amount_line(self):
        for purchase in self:
            amount_tariff = amount_vat = 0.0
            for line in purchase.import_line:
                amount_tariff += line.price_tariff
                amount_vat += line.price_tax
            purchase.update({
                'amount_tariff': purchase.currency_company_id.round(amount_tariff),
                'amount_vat': purchase.currency_company_id.round(amount_vat),
            })

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

    def action_purchase(self):
        self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})

    def action_progress(self):
        self.write({'state': 'progress'})
        for purchase in self:
            purchase._action_progress()

    def _action_progress(self):
        self.ensure_one()
        picking_ids = self.orders_ids.picking_ids.filtered(lambda p: p.state == 'assigned')
        move_lines = picking_ids.move_lines.filtered(lambda m: m.state == 'assigned')
        picking_ids.write({'import_id': self.id})
        move_lines.write({'import_id': self.id})

    def action_check(self):
        for purchase in self:
            purchase._action_check()

    def _action_check(self):
        self.ensure_one()
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.picking_ids.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        option = 'demand' if no_quantities_done else 'backorder'
        self._assign_percent(option)
        self._action_validate(option)

    def _assign_percent(self, option):
        self.ensure_one()
        moves = self.move_lines if option == 'demand' else self.move_lines.filtered(lambda m: m.quantity_done)
        total = sum((move.weight if self.price_type == 'weight' else move.price_unit) * (move.product_uom_qty if option == 'demand' else move.quantity_done) for move in moves)
        for move in moves:
            tot_move = (move.weight if self.price_type == 'weight' else move.price_unit) * (move.product_uom_qty if option == 'demand' else move.quantity_done)
            percentage = tot_move / total
            move.write({'import_percentage': percentage})

    def action_validate(self):
        self.action_purchase_order()
        # self.create_account_move('vat')
        self.moves_ids.write({'import_bool': True})
        self.picking_ids.write({'import_id': False})
        for purchase in self:
            purchase.move_lines.filtered(lambda m: m.state == 'done').write({'import_done_id': purchase.id})
        self.move_lines.write({'import_id': False})
        self.write({'state': 'done'})

    def _action_validate(self, option):
        self.ensure_one()
        moves = self.move_lines if option == 'demand' else self.move_lines.filtered(lambda m: m.quantity_done)
        self._compute_amount_cif(moves, option)
        self._action_create_line(moves, option)

    def action_draft(self):
        self.write({'state': 'draft'})

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

    def action_purchase_order(self):
        self.orders_ids.action_purchase_import()

    # Lines
    def _compute_amount_cif(self, moves, option):
        self.ensure_one()
        self.amount_cost = sum((move._get_price_unit_purchase()) * (move.product_uom_qty if option == 'demand' else move.quantity_done) for move in moves)
        if not self.amount_insurance:
            self.amount_insurance = abs(sum(move.amount_total_signed for move in self.moves_ids.filtered(lambda m: m.import_type == 'insurance')))
        if not self.amount_freight:
            self.amount_freight = abs(sum(move.amount_total_signed for move in self.moves_ids.filtered(lambda m: m.import_type == 'freight')))

    def _action_create_line(self, moves, option):
        self.ensure_one()
        self.import_line.sudo().unlink()
        import_line = []
        for move in moves:
            product_qty = move.product_uom_qty if option == 'demand' else move.quantity_done
            price_unit = move._get_price_unit_purchase() or move._get_price_unit()
            price_unit_currency = self.currency_company_id.with_context(date=self.date_import.date()).compute(price_unit, self.currency_id)
            price_cost = price_unit * product_qty
            price_cost_currency = price_unit_currency * product_qty
            price_insurance = move.import_percentage * self.amount_insurance
            price_freight = move.import_percentage * self.amount_freight
            price_cif = move.import_percentage * self.amount_cif
            price_expense = move.import_percentage * self.amount_expense
            price_customs = price_cif + price_expense
            vals = {
                'move_id': move.id,
                'order_id': move.purchase_line_id.order_id.id,
                'product_id': move.product_id.id,
                'weight': move.product_id.weight * product_qty,
                'name': move.product_id.display_name,
                'product_qty': product_qty,
                'product_uom': move.product_uom.id,
                'price_unit': price_unit,
                'price_unit_currency': price_unit_currency,
                'import_percentage': move.import_percentage,
                'price_cost': price_cost,
                'price_cost_currency': price_cost_currency,
                'price_insurance': price_insurance,
                'price_freight': price_freight,
                'price_cif': price_cif,
                'price_expense': price_expense,
                'price_customs': price_customs,
                'taxes_tariff_id': [(4, t.id) for t in move.product_id.tariff_ids.filtered(lambda t: t.country_id == self.partner_id.country_id).tax_id],
                'taxes_id': [(4, t.id) for t in move.product_id.supplier_taxes_id]
            }
            import_line.append((0, 0, vals))
        self.write({'import_line': import_line})

    def create_account_move(self, option):
        for purchase in self:
            purchase._create_account_move(option)

    def _create_account_move(self, option):
        self.ensure_one()
        taxes = self.import_line.taxes_id if option == 'vat' else self.import_line.taxes_tariff_id
        invoice_line_ids = []
        for tax in taxes:
            # compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None, is_refund=False, handle_price_include=True)
            lines = self.import_line.filtered(lambda l: l.taxes_id == tax) if option == 'vat' else self.import_line.filtered(lambda l: l.taxes_tariff_id == tax)
            price_unit = sum(line.price_tax if option == 'vat' else line.price_tariff for line in lines)
            # product = lines.product_id
            compute = tax.compute_all(price_unit)
            dics = compute.get('taxes')
            for dic in dics:
                line = {
                    'name': '[' + self.name + '] ' + dic.get('name'),
                    'account_id': dic.get('account_id'),
                    # 'price_unit': dic.get('amount'),
                    'price_unit': compute.get('total_excluded'),
                }
                invoice_line_ids.append((0,0,line))
        if invoice_line_ids:
            move = {
                'type': 'in_invoice',
                'company_id': self.company_id.id,
                'invoice_origin': self.name,
                'ref': self.partner_ref,
                'import_id': self.id,
                'import_type': 'tariff',
                'invoice_line_ids': invoice_line_ids,
            }
            am = self.env['account.move'].sudo().create(move)
            purchase = {'invoice_vat': am.id} if option == 'vat' else {'invoice_tariff': am.id}
            self.write(purchase)


class PurchaseImportLine(models.Model):
    _name = 'purchase.import.line'
    _description = 'Purchase Import Line'
    _order = 'import_id, order_id, sequence, id'

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
    weight = fields.Float('Weight', digits='Stock Weight')

    categ_id = fields.Many2one(related='product_id.categ_id', store=True)

    # Cost
    currency_import_id = fields.Many2one(related='import_id.currency_id', store=True, string='Import Currency')
    price_unit_currency = fields.Monetary('Unit Price Currency', digits='Product Price', currency_field='currency_import_id')
    price_cost_currency = fields.Monetary('Cost Price Currency', digits='Product Price', currency_field='currency_import_id')

    price_unit = fields.Monetary(string='Unit Price', required=True, digits='Product Price')
    price_subtotal = fields.Monetary(compute='_compute_price', string='Subtotal', store=True,  digits='Product Price')
    price_total = fields.Monetary(compute='_compute_price', string='Total', store=True,  digits='Product Price')
    price_tax = fields.Monetary(compute='_compute_price', string='Tax', store=True,  digits='Product Price')

    price_cost = fields.Monetary('Cost Price', digits='Product Price')
    price_insurance = fields.Monetary('Insurance Price', digits='Product Price')
    price_freight = fields.Monetary('Freight Price', digits='Product Price')
    price_cif= fields.Monetary('CIF Price', digits='Product Price')

    price_expense = fields.Monetary('Expense Price', digits='Product Price', store=True)
    price_customs = fields.Monetary('Customs Price', digits='Product Price')
    price_tariff = fields.Monetary('Tariff Price', digits='Product Price', compute='_compute_price', store=True)

    order_id = fields.Many2one('purchase.order', 'Order')
    import_id = fields.Many2one('purchase.import', string='Import Reference', index=True, required=True, ondelete='cascade')
    import_percentage = fields.Float('Import Percentage', copy=False, default=0.0)

    move_id = fields.Many2one('stock.move', 'Move')

    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    company_id = fields.Many2one('res.company', related='import_id.company_id', string='Company', store=True, readonly=True)
    state = fields.Selection(related='import_id.state', store=True, readonly=False)

    partner_id = fields.Many2one('res.partner', related='import_id.partner_id', string='Partner', readonly=True, store=True)
    currency_id = fields.Many2one(related='import_id.currency_company_id', store=True, string='Currency', readonly=True)
    date_import = fields.Datetime(related='import_id.date_import', string='Import Date', readonly=True)

    @api.depends('price_customs', 'taxes_tariff_id', 'taxes_id')
    def _compute_price(self):
        for line in self:
            # compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None, is_refund=False, handle_price_include=True)
            price_customs = line.price_customs
            taxes_tariff = line.taxes_tariff_id.compute_all(price_customs)
            price_tariff = sum(t.get('amount', 0.0) for t in taxes_tariff.get('taxes', []))
            price_vat = price_customs + price_tariff
            product = line.product_id
            partner = line.partner_id
            taxes = line.taxes_id.compute_all(price_vat, product=product, partner=partner)
            price_tax = sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
            price_total = taxes.get('total_included')
            price_subtotal = taxes.get('total_excluded')
            line.update({
                'price_tariff': price_tariff,
                'price_tax': price_tax,
                'price_subtotal': price_subtotal,
                'price_total': price_total,
            })
