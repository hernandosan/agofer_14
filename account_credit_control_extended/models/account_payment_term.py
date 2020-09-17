# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    credit_type = fields.Selection([('credit','Credit'),('cash','Cash')], 'Credit Type', compute='_compute_credit_type')

    def _compute_credit_type(self):
        for term in self:
            term.credit_type = 'credit' if term.line_ids and sum(l.days for l in term.line_ids) else 'cash'
