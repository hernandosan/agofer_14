# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    production_type = fields.Selection([('manufacturing','Manufacturing'),('production','Production')], 
        string='Manufacturing type', default='manufacturing')
    move_noproduct_ids = fields.One2many('stock.move', 'non_conforming_production_id', 'Nonconforming Products', copy=True, 
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, domain=[('scrapped', '=', False)])

    def _cal_price(self, consumed_moves):
        res = super(MrpProduction, self)._cal_price(consumed_moves)
        self.workorder_ids.create_account_move_line()
        return res

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        self.action_confirm_noproducts()
        return True

    def action_cancel(self):
        res = super(MrpProduction, self).action_cancel()
        self.move_noproduct_ids.filtered(lambda x: x.state not in ('done', 'cancel')).picking_id.action_cancel()
        return res

    def button_plan(self):
        res = super(MrpProduction, self).button_plan()
        moves = self.move_noproduct_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
        moves.picking_id.action_assign()
        moves.picking_id._action_done()
        return res

    def action_confirm_noproducts(self):
        for production in self.filtered(lambda p: p.move_noproduct_ids):
            production._action_confirm_noproducts()

    def _action_confirm_noproducts(self):
        self.ensure_one()
        for move in self.move_noproduct_ids:
            location_dest_id = self.move_noproduct_ids.location_dest_id
            domain = [('code','=','internal'),('default_location_dest_id','=',location_dest_id.id)]
            picking_type = self.env['stock.picking.type'].search(domain, limit=1)
            vals = {
                'picking_type_id': picking_type.id,
                'location_id': location_dest_id.id,
                'location_dest_id': self.location_dest_id.id,
            }
            picking = self.env['stock.picking'].create(vals)
            move.write({
                'location_id': location_dest_id.id,
                'picking_id': picking.id, 
                'move_orig_ids': [(4, id, 0) for id in self.move_finished_ids.filtered(lambda m: m.product_id.id == self.product_id.id).ids]})
            picking.action_confirm()
