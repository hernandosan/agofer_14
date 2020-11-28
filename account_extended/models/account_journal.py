# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    payment_income_account_id = fields.Many2one('account.account', check_company=True, copy=False, ondelete='restrict', 
        string='Income Receipts Account', domain=[('deprecated', '=', False), ('user_type_id.type', 'not in', ('receivable', 'payable'))])
    payment_expense_account_id = fields.Many2one('account.account', check_company=True, copy=False, ondelete='restrict', 
        string='Expense Receipts Account', domain=[('deprecated', '=', False), ('user_type_id.type', 'not in', ('receivable', 'payable'))])
