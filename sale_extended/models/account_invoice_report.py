# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    kilogram = fields.Float('Kilogram')

    _depends = {
        'product.product': ['weight'],
    }

    def _select(self):
        return super()._select() + ", product.weight * line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END) as kilogram"
