# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    import_id = fields.Many2one('purchase.import', 'Import')

    def process(self):
        if self.import_id:
            self.import_id.create_account_move('tariff')
        res = super(StockImmediateTransfer, self).process()
        if self.import_id:
            self.import_id.action_validate()
        return res


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    imports_ids = fields.Many2many('purchase.import', 'purchase_import_backorder_rel')

    def process(self):
        if self.imports_ids:
            self.imports_ids.create_account_move('tariff')
        res = super(StockBackorderConfirmation, self).process()
        if self.imports_ids:
            self.imports_ids.action_validate()
        return res
