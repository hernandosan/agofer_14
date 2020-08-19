# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        self.action_confirm_before()
        return super(SaleOrder, self).action_confirm()

    def action_confirm_before(self):
        self.validate_subtotal_standard()

    def validate_subtotal_standard(self):
        for sale in self:
            msg_validate = sale._validate_subtotal_standard()
            if msg_validate:
                # if self.env.user.has_group('sales_team.group_sale_manager'):
                #     user = self.env.user.login
                #     order = sale.name
                #     body = _("Sell below cost. user %s, order %s \n") % (user, order) + msg_validate
                #     _logger.warning(body)
                #     sale.message_post(body=body)
                # else:
                msg = _('You cannot sell below the cost of the product. \n') + msg_validate
                raise ValidationError(msg)

    def _validate_subtotal_standard(self):
        self.ensure_one()
        return self.order_line.msg_subtotal_standard()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def msg_subtotal_standard(self):
        msg = ""
        for line in self:
            price_subtotal = line.price_subtotal / line.product_uom_qty
            standard_price = line.product_id.sudo().standard_price
            if price_subtotal < standard_price:
                msg += line._msg_subtotal_standard(price_subtotal, standard_price)
        return msg

    def _msg_subtotal_standard(self, subtotal, standard):
        self.ensure_one()
        product = self.product_id.sudo().display_name
        return _("Product: %s, Subtotal: %s, Standard: %s \n") % (product, subtotal, standard)
