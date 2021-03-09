# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrBranch(models.Model):
    _inherit = 'hr.branch'

    # Sale
    sale_pricelists_ids = fields.Many2many('product.pricelist', string='Pricelists')
    sale_boolean = fields.Boolean('Modify', default=False, help="Modify the price list")
    # Stock 
    stock_warehouses_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    # Account
    account_journal_invoice_id = fields.Many2one('account.journal', 'Invoice Journal')
    account_journal_refund_id = fields.Many2one('account.journal', 'Refund Journal') 
