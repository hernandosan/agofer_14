# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    order_id = fields.Many2one('sale.order', 'Order', copy=False, ondelete="cascade")

    @api.onchange('order_id')
    def _onchange_order_id(self):
        order_id = self.order_id
        self.destination_account_id = order_id.payment_account_id if order_id else self.destination_account_id
