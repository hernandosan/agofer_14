# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def _get_default_location_dest_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self._context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_dest_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False

    production_type = fields.Selection([('manufacturing','Manufacturing'),('production','Production')], 
        string='Manufacturing type', dafult='manufacturing')
    is_decrease = fields.Boolean('Is Decrease', default=False, copy=True)
    product_second_id = fields.Many2one('product.product', 'Second Product', 
        readonly=True, check_company=True, states={'draft': [('readonly', False)]})
    product_decrease_id = fields.Many2one('product.product', 'Decrease Product', 
        readonly=True, check_company=True, states={'draft': [('readonly', False)]})
    move_finished_second_ids = fields.One2many('stock.move', 'production_second_id', 'Finished Second Products',
        copy=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, domain=[('scrapped', '=', False)])
    move_finished_decrease_ids = fields.One2many('stock.move', 'production_decrease_id', 'Finished Decrease Products',
        copy=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, domain=[('scrapped', '=', False)])
    location_dest_second_id = fields.Many2one('stock.location', 'Finished Second Products Location', default=_get_default_location_dest_id, 
        readonly=True, required=True, domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True)
    location_dest_decrease_id = fields.Many2one('stock.location', 'Finished Decrease Products Location', default=_get_default_location_dest_id, 
        readonly=True, required=True, domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True)

    def _cal_price(self, consumed_moves):
        res = super(MrpProduction, self)._cal_price(consumed_moves)
        self.workorder_ids.create_account_move_line()
        return res
