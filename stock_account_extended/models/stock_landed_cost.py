# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_bill_id = fields.Many2one('account.move', 'Vendor Bill', states={'done': [('readonly', True)]})
    order_id = fields.Many2one('purchase.order', 'Purchase Order', states={'done': [('readonly', True)]})
    lines_ids = fields.Many2many('account.move.line', string='Journal Items', compute='_compute_lines_ids')

    @api.depends('company_id')
    def _compute_allowed_picking_ids(self):
        for cost in self:
            domain = [('state','=','assigned'),('picking_type_id.code','=','internal'),('company_id','=',cost.company_id.id)]
            cost.allowed_picking_ids = self.env['stock.picking'].search(domain)

    @api.depends('picking_ids')
    def _compute_lines_ids(self):
        for cost in self:
            cost.lines_ids = cost.picking_ids.move_lines.account_move_ids.line_ids

    def get_valuation_lines(self):
        lines = super(StockLandedCost, self).get_valuation_lines()
        for line in lines:
            move_id = self.env['stock.move'].browse(line.get('move_id'))
            product_id = self.env['stock.move'].browse(line.get('product_id'))
            cost = move_id._get_price_unit() or product_id.standard_price
            cost *= line.get('quantity')
            line.update(former_cost=cost)
        return lines

    def button_validate(self):
        self._check_can_validate()
        cost_without_adjusment_lines = self.filtered(lambda c: not c.valuation_adjustment_lines)
        if cost_without_adjusment_lines:
            cost_without_adjusment_lines.compute_landed_cost()
        if not self._check_sum():
            raise UserError(_('Cost and adjustments lines do not match. You should maybe recompute the landed costs.'))

        for cost in self:
            for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
                line.move_id.write({
                    'cost_id': cost.id,
                    'price_unit': line.final_cost / line.quantity,
                    'additional_cost': line.additional_landed_cost / line.quantity,
                })

            cost.picking_ids.write({'carrier_id': cost.carrier_id.id})

            cost.write({
                'state': 'done', 
                # 'account_move_id': move.id,
            })

        return True

    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').sudo()
        result = action.read()[0]
        picking_ids = self.mapped('picking_ids')
        if picking_ids:
            result['domain'] = [('id', 'in', picking_ids.ids)]
        else:
            result = {'type': 'ir.picking.act_window_close'}
        return result

    def action_view_line(self):
        self.ensure_one()
        action_ref = self.env.ref('account.action_account_moves_all')
        if not action_ref:
            return False
        action_data = action_ref.read()[0]
        action_data['domain'] = [('id', 'in', self.lines_ids.ids)]
        return action_data
