# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    communication = fields.Char(required=False)
