# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipping_type = fields.Selection([('delivery','Delivery Agofer'),('pick','Customer Pick')], 'Shipping Type', default='delivery')

    def action_confirm(self):
        self.action_before_confirm()
        return super(SaleOrder, self).action_confirm()

    def action_before_confirm(self):
        self.validate_standard_price()
        self.validate_price_discount()
        self.validate_product_qty()
        self.validate_credit_control()

    def validate_standard_price(self):
        for sale in self:
            msg_validate = sale._validate_standard_price()
            if msg_validate:
                if self.env.user.has_group('sales_team.group_sale_manager'):
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
                if self.env.user.has_group('sales_team.group_sale_manager'):
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

    # PB0017
    def validate_price_discount(self):
        for sale in self:
            msg_validate = sale._validate_price_discount()
            if msg_validate:
                if self.env.user.has_group('sales_team.group_sale_manager'):
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

    def validate_credit_control(self):
        for sale in self:
            if sale.partner_id.credit_control:
                sale._validate_credit_quota()
                sale._validate_credit_maturity()

    def _validate_credit_quota(self):
        self.ensure_one()
        amount_total = self.company_id.currency_id.compute(self.amount_total, self.currency_id)
        credit_quota = self.partner_id.credit_quota
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
        credit_maturity = self.partner_id.credit_maturity
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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricelist_id = fields.Many2one(related='order_id.pricelist_id', store=True)
    shipping_type = fields.Selection(related='order_id.shipping_type', store=True)

    def msg_standard_price(self):
        msg = ""
        for line in self:
            price_subtotal = line.price_subtotal / line.product_uom_qty
            standard_price = line.product_id.sudo().standard_price
            if price_subtotal < standard_price:
                msg += line._msg_standard_price(price_subtotal, standard_price)
        return msg

    def _msg_standard_price(self, subtotal, standard):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        return _("Product: %s, Subtotal: %s, Standard: %s \n") % (product, subtotal, standard)

    # PB0017
    @api.onchange('discount')
    def _onchange_discount(self):
        if self.discount and self.pricelist_id:
            message = self.msg_price_discount()
            if message:
                msg = _('Order blocked by discount. \n') + message
                raise ValidationError(msg)

    def msg_price_discount(self):
        msg = ""
        for line in self:
            maximum = line.pricelist_id.discount_maximum if line.pricelist_id else 100
            freight = line.pricelist_id.discount_freight if line.pricelist_id else 100
            if line.discount > maximum + freight:
                msg += line._msg_price_discount()
            elif self.discount > maximum and self.discount <= maximum + freight:
                if line.shipping_type != 'pick':
                    msg += line._msg_price_discount()
        return msg

    def _msg_price_discount(self):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        discount = self.discount
        return _("Product: %s, Discount: %s% \n") % (product, discount)

    def msg_product_qty(self):
        msg = ""
        for line in self:
            free_qty_today = line.free_qty_today
            product_uom_qty = line.product_uom_qty
            if line.product_uom and line.product_id.uom_id and line.product_uom != line.product_id.uom_id:
                product_uom_qty = line.product_uom._compute_quantity(product_uom_qty, line.product_id.uom_id)
            if product_uom_qty > free_qty_today:
                msg += line._msg_product_qty(product_uom_qty, free_qty_today)
        return msg

    def _msg_product_qty(self, product_uom_qty, free_qty_today):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        return _("Product: %s, Quantity: %s, Available: %s \n") % (product, product_uom_qty, free_qty_today)
