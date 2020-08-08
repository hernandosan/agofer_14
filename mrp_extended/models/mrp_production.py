# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    workorders_ids = fields.Many2many('mrp.workorder', string='Works Orders', copy=False)

    def action_compute_workorders(self):
        for record in self:
            if record.workorder_ids:
                [(4, move.id) for move in self.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
                record.write({'workorders_ids': [(4, workorder.id) for workorder in record.workorder_ids]})
