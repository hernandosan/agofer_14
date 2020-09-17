# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    order_id = fields.Many2one('sale.order', 'Order', copy=False, ondelete="cascade")
