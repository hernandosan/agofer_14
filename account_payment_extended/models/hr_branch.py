# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrBranch(models.Model):
    _inherit = 'hr.branch'

    account_customer_id = fields.Many2one('account.account', 'Advance Account Customer')
    account_supplier_id = fields.Many2one('account.account', 'Advance Account Supplier')
    journal_customer_id = fields.Many2one('account.journal', 'Advance Journal Customer')
    journal_supplier_id = fields.Many2one('account.journal', 'Advance Journal Supplier')

    def _account_advance(self):
        self.ensure_one()
        return {
            'journal_customer_id': self.journal_customer_id,
            'account_customer_id': self.account_customer_id,
            'journal_supplier_id': self.journal_supplier_id,
            'account_supplier_id': self.account_supplier_id,
        }
