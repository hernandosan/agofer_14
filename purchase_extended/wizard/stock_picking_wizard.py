# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPickingWizard(models.TransientModel):
    _name = 'stock.picking.wizard'
    _description = "Stock Picking Wizard"

    def _default_products(self):
        import_id = self.env['purchase.import'].browse(self._context.get('active_ids'))
        lines = import_id.import_line.filtered(lambda line: line.product_available)
        for line in lines:
            line.write({'product_dispatch': line.product_available})
        return lines

    carrier_id = fields.Many2one('delivery.carrier','Carrier')
    warehouse_id = fields.Many2one('stock.warehouse','Destination')
    products_ids = fields.Many2many('purchase.import.line', string='Products', default=_default_products)

    def process(self):
        import_id = self.env['purchase.import'].browse(self._context.get('active_ids'))
        type_id = self.env['stock.picking.type'].search([('warehouse_id','=',self.warehouse_id.id),('code','=','incoming')], limit=1)
        location_id = self.products_ids.move_id.location_dest_id[0]
        move_lines = []
        for line in self.products_ids.filtered(lambda l: l.product_dispatch):
            dic = {
                'name': line.product_id.display_name,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom.id,
                'product_uom_qty': line.product_dispatch,
                'move_orig_ids': [(4,line.move_id.id,0)], # line.move_id
            }
            move_lines.append([0,0,dic])
            line.write({
                'product_received': line.product_received + line.product_dispatch,
                # 'product_dispatch': 0,
            })
        line = {
            'import_id': import_id.id,
            'carrier_id': self.carrier_id.id,
            'origin': import_id.name,
            'partner_id': self.warehouse_id.partner_id.id,
            'picking_type_id': type_id.id, 
            'location_id': location_id.id, 
            'location_dest_id': type_id.default_location_dest_id.id,
            'move_lines': move_lines 
        }
        self.env['stock.picking'].create(line)
        return True