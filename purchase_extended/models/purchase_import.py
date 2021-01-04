# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import ValidationError


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

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)

    currency_company_id = fields.Many2one(related='company_id.currency_id', store=True, string='Currency Company', readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES, 
        default=lambda self: self.env.company.currency_id.id)
    currency_rate = fields.Float("Currency Rate", compute='_compute_currency_rate', compute_sudo=True,  
        help='Ratio between the purchase order currency and the company currency')
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm', states={'done': [('readonly', True)]}, help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    name = fields.Char('Number', required=True, index=True, copy=False, default='New')
    notes = fields.Text('Terms and Conditions')
    origin = fields.Char('Source Document', copy=False)
    partner_id = fields.Many2one('res.partner', string='Trading', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    partner_ref = fields.Char('Reference', copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('purchase', 'Purchase Import'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    user_id = fields.Many2one('res.users', string='User', index=True, tracking=True, default=lambda self: self.env.user, check_company=True)
    # Dates
    date_import = fields.Date('Import Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Date.today())
    date_approve = fields.Date('Confirmation Date', readonly=1, index=True, copy=False)
    date_international = fields.Date(string='Port International Date', index=True)
    date_national = fields.Date(string='Port National Date', index=True)
    date_stock = fields.Date(string='Stock Date', index=True)
    # Costs
    price_type = fields.Selection([('price','Price'), ('weight','Weight')], 'Price Type', copy=False, default='price')
    allowed_order_ids = fields.Many2many('purchase.order', compute='_compute_allowed_order_ids')
    orders_ids = fields.Many2many('purchase.order', 'import_order_rel', 'import_id', 'order_id', 'Orders', states=READONLY_STATES, copy=False)
    moves_ids = fields.Many2many('account.move', 'import_move_rel', 'import_id', 'move_id', 'Invoices', copy=False)
    # Moves
    move_lines = fields.One2many('stock.move', 'import_id', 'Stock Moves', copy=False)
    move_lines_done = fields.One2many('stock.move', 'import_done_id', 'Stock Moves Done', copy=False)
    # Pickings
    picking_ids = fields.One2many('stock.picking', 'import_id', 'Stock Pickings', copy=False)
    picking_count = fields.Integer('Picking Count', compute="_compute_picking", store=True)
    # Journal Items
    account_count = fields.Integer('Journal Item Count', compute="_compute_account", copy=False, default=0, store=True)
    account_ids = fields.Many2many('account.move.line', 'import_move_line_rel', 'import_id', 'line_id', 'Journal Items', compute="_compute_account", copy=False, store=True)
    # Totals
    import_line = fields.One2many('purchase.import.line', 'import_id', string='Import Lines', copy=False)
    # Amount
    amount_cost = fields.Monetary('Cost Amount Local', currency_field='currency_company_id', compute='_compute_amount', store=True)
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
    invoice_cif = fields.Many2one('account.move', 'Invoice CIF', copy=False)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_import' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_import']))
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.import', sequence_date=seq_date) or '/'
        return super(PurchaseImport, self).create(vals)

    @api.depends('currency_company_id', 'currency_id', 'company_id', 'date_import')
    def _compute_currency_rate(self):
        for purchase in self:
            rate = purchase.currency_id._get_conversion_rate(purchase.currency_company_id, purchase.currency_id, purchase.company_id, purchase.date_import)
            purchase.currency_rate = 1 / rate

    @api.depends('move_lines_done', 'moves_ids')
    def _compute_account(self):
        for purchase in self:
            move_ids = purchase.move_lines_done.stock_valuation_layer_ids.account_move_id.line_ids.ids
            invoice_ids = purchase.moves_ids.filtered(lambda m: m.state == 'posted').line_ids.ids
            account_ids = move_ids + invoice_ids
            account_count = len(account_ids)
            lines_ids = {
                'account_ids': [(6,0,account_ids)],
                'account_count': account_count
            }
            purchase.update(lines_ids)

    @api.depends('picking_ids')
    def _compute_picking(self):
        for purchase in self:
            purchase.picking_count = len(purchase.picking_ids)

    @api.depends('import_line.price_unit', 'amount_insurance_currency', 'amount_freight_currency')
    def _compute_amount(self):
        for purchase in self:
            currency_company_id = purchase.currency_company_id
            currency_id = purchase.currency_id
            amount_cost = sum(line.price_unit for line in purchase.import_line)
            company = purchase.company_id
            date = purchase.date_import
            amount_cost_currency = currency_company_id._convert(amount_cost, currency_id, company, date)
            amount_insurance = currency_id._convert(purchase.amount_insurance_currency, currency_id, company, date)
            amount_freight = currency_id._convert(purchase.amount_freight_currency, currency_id, company, date)
            amount_cif = purchase.amount_cost + amount_insurance + amount_freight
            purchase.update({
                'amount_cost': amount_cost,
                'amount_cost_currency': amount_cost_currency,
                'amount_insurance': amount_insurance,
                'amount_freight': amount_freight,
                'amount_cif': amount_cif,
            })

    @api.depends('moves_ids.amount_total_signed')
    def _compute_expense(self):
        for purchase in self:
            expense_cost = abs(sum(move.amount_untaxed_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'cost')))
            expense_insurance = abs(sum(move.amount_untaxed_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'insurance')))
            expense_freight = abs(sum(move.amount_untaxed_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'freight')))
            expense_other = abs(sum(move.amount_untaxed_signed for move in purchase.moves_ids.filtered(lambda m: m.import_type == 'other')))
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

    @api.depends('company_id')
    def _compute_allowed_order_ids(self):
        for purchase in self:
            domain = [
                ('state', '=', 'done'), 
                ('picking_ids.state', '=', 'assigned'), 
                ('company_id', '=', purchase.company_id.id),
                ('currency_id', '=', purchase.currency_id.id)
            ]
            purchase.allowed_order_ids = self.env['purchase.order'].search(domain)

    def action_purchase(self):
        self.write({'state': 'purchase', 'date_approve': fields.Date.today()})

    def action_progress(self):
        self.write({'state': 'progress'})
        for purchase in self:
            purchase._action_progress()

    def _action_progress(self):
        self.ensure_one()
        picking_ids = self.orders_ids.picking_ids.filtered(lambda p: p.state == 'assigned')
        picking_ids.move_lines.filtered(lambda m: m.state == 'assigned').write({'import_id': self.id})

    def action_calculate(self):
        for purchase in self:
            purchase._action_calculate()

    def _action_calculate(self):
        self.ensure_one()
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_lines.picking_id.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        option = 'demand' if no_quantities_done else 'backorder'
        moves = self.move_lines if option == 'demand' else self.move_lines.filtered(lambda m: m.quantity_done)
        self._assign_percent(moves, option)
        self._action_lines(moves, option)

    def _assign_percent(self, moves, option):
        self.ensure_one()
        total = sum((move.weight if self.price_type == 'weight' else move.price_unit) * (move.product_uom_qty if option == 'demand' else move.quantity_done) for move in moves)
        if not total:
            raise ValidationError(_("Price or Weight wrong, please check"))
        for move in moves:
            tot_move = (move.weight if self.price_type == 'weight' else move.price_unit) * (move.product_uom_qty if option == 'demand' else move.quantity_done)
            percentage = tot_move / total
            move.write({'import_percentage': percentage})
    
    def _action_lines(self, moves, option):
        self.ensure_one()
        self.import_line.sudo().unlink()
        self.move_lines.sudo().write({'import_line_id': False})
        currency_id = self.currency_id
        currency_company_id = self.currency_company_id
        amount_insurance = currency_id._convert(self.amount_insurance_currency, currency_company_id, self.company_id, self.date_import)
        amount_freight = currency_id._convert(self.amount_freight_currency, currency_company_id, self.company_id, self.date_import)
        amount_expense = self.amount_expense
        for move in moves:
            product_qty = move.product_uom_qty if option == 'demand' else move.quantity_done
            price_unit = move._get_price_unit_purchase() or move._get_price_unit()
            price_cost = price_unit * product_qty
            price_insurance = move.import_percentage * amount_insurance
            price_freight = move.import_percentage * amount_freight
            price_cif = price_cost + price_insurance + price_freight
            price_expense = move.import_percentage * amount_expense
            price_customs = price_cif + price_expense
            vals = {
                'import_id': self.id,
                'import_percentage': move.import_percentage,
                'move_id': move.id,
                'order_id': move.purchase_line_id.order_id.id,
                'line_id': move.purchase_line_id.id,
                'product_id': move.product_id.id,
                'weight': move.product_id.weight * product_qty,
                'name': move.product_id.display_name,
                'product_qty': product_qty,
                'product_uom': move.product_uom.id,
                'price_unit': price_unit,
                'price_cost': price_cost,
                'price_insurance': price_insurance,
                'price_freight': price_freight,
                'price_cif': price_cif,
                'price_expense': price_expense,
                'price_customs': price_customs,
                'taxes_tariff_id': [(4, t.id) for t in move.product_id.tariff_ids.filtered(lambda t: t.country_id == self.partner_id.country_id).tax_id],
                'taxes_id': [(4, t.id) for t in move.product_id.supplier_taxes_id]
            }
            import_line = self.env['purchase.import.line'].create(vals)
            move.write({'import_line_id': import_line})

    def action_validate(self):
        for purchase in self:
            purchase._action_validate()

    def _action_validate(self):
        self.ensure_one()
        self.move_lines.filtered(lambda m: m.state == 'done').write({'import_done_id': self.id})
        self.move_lines.write({'import_id': False})
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.move_lines.write({'import_id': False, 'import_line_id': False})
        self.write({'state': 'cancel'})

    def button_validate(self):
        self.ensure_one()

        if not self.import_line:
            raise UserError(_('Please calculate items first.'))

        if not self.move_lines:
            raise UserError(_('Please add some items to move.'))

        self.import_line.action_validate()

        return self.with_context(import_id=self.id).move_lines.picking_id.button_validate()

    def action_invoice(self):
        for purchase in self:
            purchase._invoice_cif()
            # purchase._invoice_tax('vat')

    def _invoice_cif(self):
        self.ensure_one()
        partner_id = self.partner_id
        # Copy purchase lines
        invoice = {
            'date': self.date_import,
            'move_type': 'in_invoice',
            'company_id': self.company_id.id,
            'import_id': self.id,
            'import_type': 'cif',
            'partner_id': partner_id.id,
            'invoice_origin': self.name,
            'ref': self.partner_ref,
            # Partner
            'fiscal_position_id': partner_id.property_account_position_id.id if partner_id.property_account_position_id else False,
            'invoice_payment_term_id': partner_id.property_supplier_payment_term_id.id if partner_id.property_supplier_payment_term_id else False,
            'currency_id': self.currency_id.id,
        }
        invoice_id = self.env['account.move'].sudo().create(invoice)
        invoice_line_ids = []
        for line in self.import_line:
            lines = line.line_id._prepare_account_move_line(invoice_id)
            # account
            accounts = line.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=self.env['account.fiscal.position'].browse(invoice.get('fiscal_position_id')))
            lines.update(quantity=line.product_qty, account_id=accounts['expense'])
            invoice_line_ids.append((0,0,lines))
        if self.amount_insurance_currency:
            product_id = self.env.ref('purchase_extended.product_product_insurance')
            lines = {
                'name': '%s: %s' % (self.name, product_id.display_name),
                'move_id': invoice_id.id,
                'currency_id': self.currency_id,
                'date_maturity': invoice_id.invoice_date_due,
                'product_uom_id': product_id.uom_id.id,
                'product_id': product_id.id,
                'price_unit': self.amount_insurance_currency,
                'quantity': 1.0,
                'partner_id': invoice_id.partner_id.id,
            }
            invoice_line_ids.append((0,0,lines))
        if self.amount_freight_currency:
            product_id = self.env.ref('purchase_extended.product_product_freight')
            lines = {
                'name': '%s: %s' % (self.name, product_id.display_name),
                'move_id': invoice_id.id,
                'currency_id': self.currency_id,
                'date_maturity': invoice_id.invoice_date_due,
                'product_uom_id': product_id.uom_id.id,
                'product_id': product_id.id,
                'price_unit': self.amount_freight_currency,
                'quantity': 1.0,
                'partner_id': invoice_id.partner_id.id,
            }
            invoice_line_ids.append((0,0,lines))
        invoice_id.write({'invoice_line_ids': invoice_line_ids})
        self.update({'invoice_cif': invoice_id.id})

    def _invoice_tax(self, option):
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
                'move_type': 'in_invoice',
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

    def action_view_account(self):
        action = self.env.ref('account.action_account_moves_all').sudo()
        result = action.read()[0]
        # choose the view_mode accordingly
        account_ids = self.mapped('account_ids')
        if account_ids:
            result['domain'] = [('id', 'in', account_ids.ids)]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').sudo()
        result = action.read()[0]
        picking_ids = self.mapped('picking_ids')
        if picking_ids:
            result['domain'] = [('id', 'in', picking_ids.ids)]
        else:
            result = {'type': 'ir.picking.act_window_close'}
        return result


class PurchaseImportLine(models.Model):
    _name = 'purchase.import.line'
    _description = 'Purchase Import Line'
    _order = 'import_id, order_id, sequence, id'

    categ_id = fields.Many2one(related='product_id.categ_id', store=True)

    company_id = fields.Many2one('res.company', related='import_id.company_id', string='Company', store=True, readonly=True)

    currency_id = fields.Many2one(related='import_id.currency_company_id', store=True, string='Currency', readonly=True)
    currency_import_id = fields.Many2one(related='import_id.currency_id', store=True, string='Import Currency')

    date_import = fields.Date(related='import_id.date_import', string='Import Date', store=True, readonly=True)
    date_planned = fields.Datetime(string='Scheduled Date', index=True)

    import_id = fields.Many2one('purchase.import', string='Import Reference', index=True, required=True, ondelete='cascade')
    import_percentage = fields.Float('Import Percentage', copy=False, default=0.0)

    line_id = fields.Many2one('purchase.order.line', 'Order Line', ondelete='set null', index=True, readonly=True)

    move_id = fields.Many2one('stock.move', 'Move')

    name = fields.Char(string='Description', required=True)

    order_id = fields.Many2one('purchase.order', 'Order', ondelete='set null', index=True, readonly=True)

    partner_id = fields.Many2one(related='import_id.partner_id', string='Partner', readonly=True, store=True)

    price_additional = fields.Monetary('Additional Price')
    price_cif= fields.Monetary('CIF Price')
    price_cost = fields.Monetary('Cost Price', required=True)
    price_cost_currency = fields.Monetary('Cost Price Currency', currency_field='currency_import_id', compute='_compute_price_currency')
    price_customs = fields.Monetary('Customs Price')
    price_expense = fields.Monetary('Expense Price')
    price_freight = fields.Monetary('Freight Price', required=True)
    price_freight_currency = fields.Monetary('Freight Price Currency', currency_field='currency_import_id', compute='_compute_price_currency')
    price_insurance = fields.Monetary('Insurance Price', required=True)
    price_insurance_currency = fields.Monetary('Insurance Price Currency', currency_field='currency_import_id', compute='_compute_price_currency')
    price_subtotal = fields.Monetary(compute='_compute_price', string='Subtotal')
    price_tariff = fields.Monetary('Tariff Price', compute='_compute_price')
    price_tax = fields.Monetary(compute='_compute_price', string='Tax')
    price_total = fields.Monetary(compute='_compute_price', string='Total')
    price_unit = fields.Monetary('Unit Price', required=True)
    price_unit_additional = fields.Monetary('Unit Price Additional')
    price_unit_currency = fields.Monetary('Unit Price Currency', currency_field='currency_import_id', compute='_compute_price_currency')
    price_unit_subtotal = fields.Monetary('Unit Price Subtotal')

    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True)
    product_type = fields.Selection(related='product_id.type', store=True, readonly=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', store=True)
    product_uom_qty = fields.Float(string='Total Quantity', compute='_compute_product_uom_qty', store=True)

    sequence = fields.Integer(string='Sequence', default=10)
    
    state = fields.Selection(related='import_id.state', readonly=False, store=True)

    taxes_id = fields.Many2many('account.tax', string='Taxes')
    taxes_tariff_id = fields.Many2many('account.tax', 'tax_import_res', string='Taxes tariff')

    weight = fields.Float('Weight', digits='Stock Weight')

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
            price_subtotal = taxes.get('total_excluded')
            price_total = taxes.get('total_included')
            price_additional = price_subtotal - line.price_cost
            # Unit 
            price_unit_subtotal = price_subtotal / line.product_qty
            price_unit_additional = price_additional / line.product_qty
            line.update({
                'price_tariff': price_tariff,
                'price_tax': price_tax,
                'price_subtotal': price_subtotal,
                'price_total': price_total,
                'price_additional': price_additional,
                'price_unit_subtotal': price_unit_subtotal,
                'price_unit_additional': price_unit_additional,
            })

    @api.depends('price_unit', 'price_cost', 'price_insurance', 'price_freight')
    def _compute_price_currency(self):
        for line in self:
            price_unit = line.price_unit
            price_cost = line.price_cost
            price_insurance = line.price_insurance
            price_freight = line.price_freight
            company = line.company_id
            date = line.date_import
            price_unit_currency = line.currency_id._convert(price_unit, line.currency_import_id, company, date)
            price_cost_currency = line.currency_id._convert(price_cost, line.currency_import_id, company, date)
            price_insurance_currency = line.currency_id._convert(price_insurance, line.currency_import_id, company, date)
            price_freight_currency = line.currency_id._convert(price_freight, line.currency_import_id, company, date)
            line.update({
                'price_unit_currency': price_unit_currency,
                'price_cost_currency': price_cost_currency,
                'price_insurance_currency': price_insurance_currency,
                'price_freight_currency': price_freight_currency,
            })

    def action_validate(self):
        for line in self:
            line._action_validate()

    def _action_validate(self):
        self.ensure_one()
        price_unit = self.price_subtotal / self.product_qty
        self.move_id.write({'price_unit': price_unit})
