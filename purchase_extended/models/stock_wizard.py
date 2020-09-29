# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        if self.env.context.get('import_id'):
            self.env['purchase.import'].browse(self.env.context.get('import_id'))._invoice_tax('tariff')
        res = super(StockImmediateTransfer, self).process()
        if self.env.context.get('import_id'):
            self.env['purchase.import'].browse(self.env.context.get('import_id'))._action_validate()
        return res


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self):
        if self.env.context.get('import_id'):
            self.env['purchase.import'].browse(self.env.context.get('import_id'))._invoice_tax('tariff')
        res = super(StockBackorderConfirmation, self).process()
        if self.env.context.get('import_id'):
            self.env['purchase.import'].browse(self.env.context.get('import_id'))._action_validate()
        return res
