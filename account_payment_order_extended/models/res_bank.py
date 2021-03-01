# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    report_id = fields.Many2one('ir.actions.report', 'Report')
