from odoo import fields, models, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    report_id = fields.Many2one('ir.actions.report', 'Report')
