# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    import_id = fields.Many2one('purchase.import', 'Import', copy=False)
