# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def create(self, vals):
        payment = super(AccountPayment, self).create(vals)
        payment.write(vals)
        return payment
