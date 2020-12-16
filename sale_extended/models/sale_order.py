# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    credit_type = fields.Selection(related='payment_term_id.credit_type', store=True)
    shipping_bool = fields.Boolean('Shipping Bool', copy=False)
    shipping_type = fields.Selection([('delivery','Delivery Agofer'),('pick','Customer Pick')], 'Shipping Type', default='delivery')
    pick_bool = fields.Boolean('Pick Bool')
    pick_date = fields.Date('Pick Date')
    upload_date = fields.Date('Upload Date')
    upload_delay = fields.Float('Customer Upload Time', compute='_compute_delay')
    delivery_bool = fields.Boolean('Delivery Bool')
    delivery_assistant = fields.Boolean('Delivery Assistant')
    delivery_date = fields.Date('Delivery Date')
    delivery_delay = fields.Float('Customer Delivery Time', compute='_compute_delay')
    # Payment
    payments_id = fields.One2many('account.payment', 'order_id', 'Payments')
    payment_journal_id = fields.Many2one(related='team_id.advance_journal_id')
    payment_account_id = fields.Many2one(related='team_id.advance_account_id')
    # Team
    teams_ids = fields.Many2many(related='user_id.teams_ids')
    # Pricelist
    pricelists_ids = fields.Many2many(related='team_id.pricelists_ids')
    # Stock
    warehouses_ids = fields.Many2many(related='team_id.warehouses_ids')

    @api.depends('order_line.upload_delay', 'order_line.delivery_delay')
    def _compute_delay(self):
        for sale in self:
            upload_delay = max(line.upload_delay for line in sale.order_line) if sale.order_line else 0
            delivery_delay = max(line.delivery_delay for line in sale.order_line) if sale.order_line else 0
            sale.update({'upload_delay': upload_delay, 'delivery_delay': delivery_delay})

    @api.onchange('date_order')
    def _onchange_date_order(self):
        if self.date_order:
            self.upload_date = self.date_order + timedelta(days=self.delivery_delay or 2)

    @api.onchange('upload_date')
    def _onchange_upload_date(self):
        if self.upload_date:
            self.delivery_date = self.upload_date + timedelta(days=self.delivery_delay or 1)

    def copy(self, default=None):
        if not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            default = dict(default or {})
            pricelist_id = self.warehouse_id.pricelists_ids[0].id if self.warehouse_id.pricelists_ids else False
            if pricelist_id:
                default.update(pricelist_id=self.warehouse_id.pricelists_ids[0].id)
        return super(SaleOrder, self).copy(default)

    def action_confirm(self):
        self.action_before_confirm()
        res = super(SaleOrder, self).action_confirm()
        self.action_after_confirm()
        return res

    def action_before_confirm(self):
        self.validate_price_discount()
        self.validate_standard_price()
        self.validate_product_qty()
        self.validate_delivery_date()
        self.validate_credit_type()

    def action_after_confirm(self):
        # self.action_quotation_send()
        self.send_shipping_date()

    def validate_price_discount(self):
        for sale in self:
            msg_validate = sale._validate_price_discount()
            if msg_validate:
                if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                    user = self.env.user.login
                    order = sale.name
                    body = _("Order confirmed by discount. User: %s, Order: %s \n") % (user, order) + msg_validate
                    _logger.warning(body)
                    sale.message_post(body=body)
                else:
                    msg = _('Order blocked by discount. \n') + msg_validate
                    raise ValidationError(msg)

    def _validate_price_discount(self):
        self.ensure_one()
        return self.order_line.msg_price_discount()

    def validate_standard_price(self):
        for sale in self:
            msg_validate = sale._validate_standard_price()
            if msg_validate:
                if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                    user = self.env.user.login
                    order = sale.name
                    body = _("Order confirmed by cost. User: %s, Order: %s \n") % (user, order) + msg_validate
                    _logger.warning(body)
                    sale.message_post(body=body)
                else:
                    msg = _('Order blocked by cost of product. \n') + msg_validate
                    raise ValidationError(msg)

    def _validate_standard_price(self):
        self.ensure_one()
        return self.order_line.msg_standard_price()

    def validate_product_qty(self):
        for sale in self:
            msg_validate = sale._validate_product_qty()
            if msg_validate:
                if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                    user = self.env.user.login
                    order = sale.name
                    body = _("Order confirmed by quanity. User %s, Order %s \n") % (user, order) + msg_validate
                    _logger.warning(body)
                    sale.message_post(body=body)
                else:
                    msg = _('Order blocked by quanity. \n') + msg_validate
                    raise ValidationError(msg)

    def _validate_product_qty(self):
        self.ensure_one()
        return self.order_line.msg_product_qty()

    def validate_delivery_date(self):
        for sale in self:
            sale._validate_delivery_date()

    def _validate_delivery_date(self):
        self.ensure_one()
        date_order = self.date_order.date()
        weekday = date_order.weekday()
        days = 3 if weekday not in (3, 4, 5) else 4
        date = date_order + timedelta(days=days)
        if not self.delivery_bool and self.delivery_date and self.delivery_date < date:
            if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                user = self.env.user.login
                order = self.name
                body = _("Order confirmed by days. User: %s, Order: %s") % (user, order)
                _logger.warning(body)
                self.message_post(body=body)
            else:
                msg = _("Order blocked by days. Delivery date cannot be less than three days")
                raise ValidationError(msg)

    def validate_credit_type(self):
        for sale in self:
            sale.validate_cash_control() if sale.credit_type == 'cash' else sale.validate_credit_control()

    def validate_cash_control(self):
        for sale in self:
            sale._validate_cash_control()

    def _validate_cash_control(self):
        self.ensure_one()
        decimal_places = self.currency_id.decimal_places
        amount_total = self.amount_total
        amount_payment = sum(payment.currency_id.with_context(date=payment.date).compute(payment.amount, self.currency_id) for payment in self._sale_payments_id()) or 0.0
        if amount_payment < amount_total:
            if self.env.user.has_group('account_credit_control.group_account_credit_control_user'):
                user = self.env.user.login
                order = self.name
                body = _("Order confirmed by cash. User: %s, Order: %s") % (user, order)
                _logger.warning(body)
                self.message_post(body=body)
            else:
                msg = _("Order blocked by cash. Total: $ %s, Payment: $ %s") % (round(amount_total,decimal_places), round(amount_payment,decimal_places))
                raise ValidationError(msg)

    def validate_credit_control(self):
        for sale in self:
            if sale.partner_id.commercial_partner_id.credit_control:
                sale._validate_credit_quota()
                sale._validate_credit_maturity()

    def _validate_credit_quota(self):
        self.ensure_one()
        amount_total = self.currency_id.with_context(date=self.date_order).compute(self.amount_total, self.company_id.currency_id)
        credit_quota = self.partner_id.commercial_partner_id.credit_quota
        decimal_places = self.company_id.currency_id.decimal_places
        if amount_total > credit_quota:
            if self.env.user.has_group('account_credit_control.group_account_credit_control_user'):
                user = self.env.user.login
                order = self.name
                body = _("Order confirmed by quota. User: %s, Order: %s") % (user, order)
                _logger.warning(body)
                self.message_post(body=body)
            else:
                msg = _("Order blocked by quota. Quota: $ %s, Value: $ %s") % (round(credit_quota,decimal_places), round(amount_total,decimal_places))
                raise ValidationError(msg)

    def _validate_credit_maturity(self):
        self.ensure_one()
        credit_maturity = self.partner_id.commercial_partner_id.credit_maturity
        if credit_maturity:
            if self.env.user.has_group('account_credit_control.group_account_credit_control_user'):
                user = self.env.user.login
                order = self.name
                body = _("Order confirmed by maturity. User: %s, Order: %s") % (user, order)
                _logger.warning(body)
                self.message_post(body=body)
            else:
                msg = _("Order blocked by maturity. Maturity: $ %s") % (credit_maturity)
                raise ValidationError(msg)

    def run_reservation(self):
        incoterm = self.env.ref('sale_extended.incoterm_res').id
        date = datetime.now() - timedelta(days=15)
        sales = self.search([('state','=','done'),('incoterm','=',incoterm),('date_order','<=',date),('shipping_bool','=',False)])
        sales.action_reservation()

    def action_reservation(self):
        for sale in self:
            sale._action_reservation()

    def _action_reservation(self):
        self.ensure_one()
        vals = {
            'res_id': self.id,
            'res_model_id': self.env['ir.model']._get('sale.order').id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'date_deadline': fields.Date.today(),
            'user_id': self.user_id.id if self.user_id else self.create_user.id,
            'summary': _('Check Sale Order'),
            'note': _('Order reserved for more than 15 days. Confirm or Cancel')
        }
        self.env['mail.activity'].sudo().create(vals)
        self.write({'shipping_bool': True})

    def action_sale_register_payment(self):
        return self.env['account.payment'].with_context(active_ids=self.ids, active_model='sale.order', active_id=self.id).action_register_payment()

    def send_shipping_date(self):
        for sale in self:
            sale._send_shipping_date()

    def _send_shipping_date(self):
        self.ensure_one()
        vals = {
            'incoterm': self.incoterm.id if self.incoterm else False,
            'shipping_type': self.shipping_type,
            'pick_bool': self.pick_bool,
            'pick_date': self.pick_date,
            'upload_date': self.upload_date,
            'delivery_bool': self.delivery_bool,
            'delivery_assistant': self.delivery_assistant,
            'delivery_date': self.delivery_date,
            # 'commitment_date': self.delivery_date,
            'note': self.note,
        }
        self.picking_ids.write(vals)

    def _sale_payments_id(self):
        self.ensure_one()
        return self.payments_id.filtered(lambda p: p.state == 'posted')

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        journal_id = self.team_id._team_invoice_journal_id()
        invoice_vals.update(journal_id=journal_id.id)
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float(copy=False)
    price_kg = fields.Float('Kg Price', digits='Product Price', compute='_compute_price_kg')
    pricelist_id = fields.Many2one(related='order_id.pricelist_id', store=True)
    shipping_type = fields.Selection(related='order_id.shipping_type', store=True)
    upload_delay = fields.Float(related='product_id.upload_delay', store=True)
    delivery_delay = fields.Float(related='product_id.delivery_delay', store=True)

    @api.onchange('discount')
    def _onchange_discount(self):
        if self.discount and self.pricelist_id:
            message = self.msg_price_discount()
            if message:
                msg = _('Order blocked by discount. \n') + message
                raise ValidationError(msg)

    @api.depends('product_uom', 'price_unit', 'product_id')
    def _compute_price_kg(self):
        for line in self:
            line.price_kg = line.product_uom._compute_price(line.price_unit, line.product_id.uom_id) / line.product_id.weight if line.product_uom and line.price_unit and line.product_id and line.product_id.weight else 0.0

    def msg_standard_price(self):
        msg = ""
        for line in self:
            price_subtotal = line.price_subtotal / line.product_uom_qty
            standard_price = line.product_id.sudo().standard_price
            if price_subtotal < standard_price:
                msg += line._msg_standard_price(price_subtotal)
        return msg

    def _msg_standard_price(self, subtotal):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        return _("Product: %s, Subtotal: $ %s \n") % (product, subtotal)

    def msg_price_discount(self):
        msg = ""
        for line in self:
            maximum = line.pricelist_id.discount_maximum if line.pricelist_id else 100
            freight = line.pricelist_id.discount_freight if line.pricelist_id else 100
            if line.discount > maximum + freight:
                msg += line._msg_price_discount()
            elif line.discount > maximum and line.discount <= maximum + freight:
                if line.shipping_type != 'pick':
                    msg += line._msg_price_discount()
        return msg

    def _msg_price_discount(self):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        discount = self.discount
        return _("Product: %s, Discount: %s \n") % (product, discount)

    def msg_product_qty(self):
        msg = ""
        for line in self:
            free_qty_today = line.free_qty_today
            product_uom_qty = line.product_uom_qty
            # if line.product_uom and line.product_id.uom_id and line.product_uom != line.product_id.uom_id:
            #     product_uom_qty = line.product_uom._compute_quantity(product_uom_qty, line.product_id.uom_id)
            if product_uom_qty > free_qty_today:
                msg += line._msg_product_qty(product_uom_qty, free_qty_today)
        return msg

    def _msg_product_qty(self, product_uom_qty, free_qty_today):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        return _("Product: %s, Quantity: %s, Available: %s \n") % (product, product_uom_qty, free_qty_today)
