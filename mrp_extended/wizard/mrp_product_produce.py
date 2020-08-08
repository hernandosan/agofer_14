# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.model
    def default_get(self, fields):
        res = super(MrpProductProduce, self).default_get(fields)
        production = self.env['mrp.production']
        production_id = self.env.context.get('default_production_id') or self.env.context.get('active_id')
        if production_id:
            production = self.env['mrp.production'].browse(production_id)
        if production.exists() and production.workorder_ids:
            # res.update(production_workorders_ids=[(4, workorder.id) for workorder in production.workorder_ids])
            if 'production_workorder_bool' in fields:
                res.update(production_workorder_bool=True)
        return res

    production_workorder_bool = fields.Boolean('Have Work Orders')
    # production_workorders_ids = fields.Many2many('mrp.workorder', string='Works Orders')

    def do_produce_workorder(self):
        self.ensure_one()
        self._before_production_workorder()
        self._record_production_workorder()
        self._check_company()
        return {'type': 'ir.actions.act_window_close'}

    def _before_production_workorder(self):
        for line in self.raw_workorder_line_ids:
            if line.product_id.tracking != 'none' and not line.lot_id:
                raise UserError(_('Please enter a lot or serial number for %s !' % self.product_id.display_name))
            if line.lot_id and line.product_id.tracking == 'serial': # and line.lot_id in self.move_id.move_line_ids.filtered(lambda ml: ml.qty_done).mapped('lot_id'):
                raise UserError(_('You cannot consume the same serial number twice. Please correct the serial numbers encoded.'))
    
    def _record_production_workorder(self):
        production_id = self.production_id
        flag = True if production_id.workorders_ids else False
        workorders = production_id.workorders_ids if flag else production_id.workorder_ids
        for workorder in workorders:
            workorder.button_start()
            for time in workorder.time_ids:
                date_end = time.date_start + timedelta(minutes=workorder.duration_real or workorder.duration_expected)
                time.write({'date_end': date_end})
            for raw in workorder.raw_workorder_line_ids:
                for line in self.raw_workorder_line_ids.filtered(lambda l: l.product_id == raw.product_id):
                    raw.write({'lot_id': line.lot_id.id and line.lot_id or False})
            workorder.write({'qty_producing': self.qty_producing})
            workorder.record_production()
