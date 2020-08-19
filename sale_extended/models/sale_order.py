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
        self.sell_below_cost()

    def sell_below_cost(self):
        self.order_line.sell_below_cost()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def sell_below_cost(self):
        for line in self:
            price_subtotal = line.price_subtotal
            standard_price = line.product_id.sudo().standard_price
            if price_subtotal < standard_price:
                # if self.env.user.has_group('sales_team.group_sale_manager'):
                #     user = self.env.user.login
                #     order = line.order_id.name
                #     _logger.warning(_("Sell below cost. user %s, order %s") % (user, order))
                # else:
                dic = line.product_id.read()[0]
                product = dic.get('display_name') or line.product_id.name
                raise ValidationError(_("You cannot sell below the cost of the product. %s (%s)") % (product, standard_price))
