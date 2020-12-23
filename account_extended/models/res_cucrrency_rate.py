# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    rate_inv = fields.Float('Rate Inverse', default=1, compute='_compute_rate_inv', inverse='_inverse_rate_inv')

    @api.depends('rate')
    def _compute_rate_inv(self):
        for rate in self:
            rate.update({'rate_inv': 1 / rate.rate})

    def _inverse_rate_inv(self):
        for rate in self:
            rate.update({'rate': 1 / rate.rate_inv})
