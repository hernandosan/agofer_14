# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPickingWizard(models.TransientModel):
    _name = 'stock.picking.wizard'
    _description = "Stock Picking Wizard"

    carrier_id = fields.Many2one('delivery.carrier','Carrier')
    import_id = fields.Many2one('purchase.import', 'Import', default=lambda self: self.env['purchase.import'].browse(self._context.get('active_ids')))
    line_ids = fields.One2many('stock.picking.line.wizard', 'picking_id', 'Lines')
    warehouse_id = fields.Many2one('stock.warehouse','Destination')

    @api.onchange('import_id')
    def _onchange_import_id(self):
        if self.import_id:
            line_ids = []
            for move in self.import_id.move_lines_done:
                available = self._compute_available(move)
                consume = self._compute_consume(move)
                if available:
                    vals = {
                        'picking_id': self.id,
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'qty_available': available,
                        'qty_consume': consume,
                        'qty_done': available,
                    }
                    self.env['stock.picking.line.wizard'].create(vals)

    def _compute_available(self, move):
        self.ensure_one()
        domain = [('move_orig_ids','=',move.id),('state','=','done'),('product_id','=',move.product_id.id)]
        moves = self.env['stock.move'].search(domain)
        done = sum(move.quantity_done for move in moves) or 0
        return move.quantity_done - done

    def _compute_consume(self, move):
        self.ensure_one()
        domain = [('move_orig_ids','=',move.id),('state','=','done'),('product_id','=',move.product_id.id)]
        moves = self.env['stock.move'].search(domain)
        return sum(move.should_consume_qty for move in moves) or 0

    def process(self):
        type_id = self.env['stock.picking.type'].search([('warehouse_id','=',self.warehouse_id.id),('code','=','internal')], limit=1)
        location_id = self.line_ids.move_id.location_dest_id[0]
        move_lines = []
        for line in self.line_ids.filtered(lambda l: l.qty_done):
            vals = {
                'name': line.product_id.display_name,
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.qty_done,
                'move_orig_ids': [(4,line.move_id.id,0)], # line.move_id
            }
            move_lines.append((0,0,vals))
        if move_lines:
            picking = {
                'import_id': self.import_id.id,
                'carrier_id': self.carrier_id.id,
                'origin': self.import_id.name,
                'partner_id': self.warehouse_id.partner_id.id,
                'picking_type_id': type_id.id, 
                'location_id': location_id.id, 
                'location_dest_id': type_id.default_location_dest_id.id,
                'move_lines': move_lines 
            }
            picking = self.env['stock.picking'].create(picking)
            picking.action_confirm()
            picking.action_assign()
        return True

class StockPickingLineWizard(models.TransientModel):
    _name = 'stock.picking.line.wizard'
    _description = "Stock Picking Line Wizard"

    move_id = fields.Many2one('stock.move', 'Move')
    picking_id = fields.Many2one('stock.picking.wizard', 'Picking', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Prodcut', readonly=True)
    product_weight = fields.Float('Weight', digits='Stock Weight', compute='_compute_product_weight')
    qty_available = fields.Float('Available', digits='Product Unit of Measure', readonly=True)
    qty_consume = fields.Float('Consume', digits='Product Unit of Measure', readonly=True)
    qty_done = fields.Float('Done', digits='Product Unit of Measure')

    @api.depends('product_id', 'qty_done')
    def _compute_product_weight(self):
        for line in self:
            line.product_weight = line.product_id.weight * line.qty_done if line.product_id.weight * line.qty_done else 0.0
