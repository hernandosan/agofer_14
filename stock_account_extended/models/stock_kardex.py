# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockKardex(models.Model):
    _name = 'stock.kardex'
    _description = 'Stock Kardex'

    company_id = fields.Many2one('res.company', 'Company', readonly=True, required=True, default=lambda self: self.env.company)
    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', 'Product', ondelete='set null')
    location_id = fields.Many2one('stock.location', 'Location', ondelete='set null')
    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To', default=fields.Datetime.now())
    kardex_ids = fields.One2many('stock.kardex.line', 'kardex_id', 'Lines')

    def action_compute(self):
        self._action_compute()

    def _action_compute(self):
        self.ensure_one()
        self.kardex_ids.sudo().unlink()

        # Before
        domain = [
            '|',
            ('location_id','=',self.location_id.id),
            ('location_dest_id','=',self.location_id.id),
            ('state','=','done'),
            ('product_id','=',self.product_id.id),
            ('date','<=',self.date_to)
        ]
        move = self.env['stock.move'].sudo().search(domain, order='date asc', limit=1)
        standard_price = move.standard_price or 0.0
        quantity = self.product_id.sudo().with_context(to_date=self.date_from).qty_available

        # Moves
        domain = [
            '|',
            ('location_id','=',self.location_id.id),
            ('location_dest_id','=',self.location_id.id),
            ('state','=','done'), 
            ('product_id','=',self.product_id.id),
            ('date','>=',self.date_from),
            ('date','<=',self.date_to)
        ]
        moves = self.env['stock.move'].sudo().search(domain, order='date asc')
        # valuations = self.env['stock.valuation.layer'].sudo().search([('stock_move_id','=',moves.ids)], order='create_date asc')
        kardex_ids = []
        for move in moves:
             # Compute
            qty_done = - move.quantity_done if move._is_out() else move.quantity_done
            qty_init = quantity
            qty_out = quantity + qty_done
            price_unit = move._get_price_unit()
            price_total = price_unit * qty_done
            # AVCO
            move_type = self._get_valued_types(move)
            standard_price = move.standard_price
            quantity = qty_out
            standard_total = standard_price * quantity
            quantity = qty_out
            vals = {
                'stock_move_id': move.id,
                'date': move.date,
                'product_id': move.product_id.id,
                'kardex_type': move_type,
                'location_id': move.location_id.id,
                'location_dest_id': move.location_dest_id.id,
                'qty_init': qty_init,
                'quantity': qty_done,
                'qty_end': qty_out,
                'price_unit': price_unit,
                'price_total': price_total,
                'standard_price': standard_price,
                'value_total': standard_total,
            }
            kardex_ids.append((0,0,vals))
        self.write({'kardex_ids': kardex_ids})

    def _get_valued_types(self, move_id):
        if move_id._is_in():
            if move_id._is_returned('in'):
                return 'in_returned'
            else:
                return 'in'
        elif move_id._is_out():
            if move_id._is_returned('out'):
                return 'out_returned'
            else:
                return 'out'
        elif move_id._is_int():
            return 'int' 
        else:
            return 'none'

    def action_kardex_line(self):
        action = self.env.ref('stock_account_extended.action_stock_kardex_line').sudo()
        result = action.read()[0]
        result['domain'] = [('kardex_id', 'in', self.id)]
        return result

class StockKardexLine(models.Model):
    _name = 'stock.kardex.line'
    _description = 'Stock Kardex Line'

    kardex_id = fields.Many2one('stock.kardex', 'Kardex', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', 'Company', related='kardex_id.company_id', readonly=True)
    date = fields.Datetime('Date')
    product_id = fields.Many2one('product.product', 'Product', readonly=True, required=True, check_company=True)
    kardex_type = fields.Selection([('none', 'None'), ('in', 'Purchase'), ('out', 'Sale'), ('in_returned', 'Purchase Returned'), ('out_returned', 'Sale Returned')], 'Type')
    location_id = fields.Many2one('stock.location', 'Source Location', check_company=True, help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.")
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', check_company=True, help="Location where the system will stock the finished products.")
    qty_init = fields.Float('Quantity Init', digits=0, readonly=True)
    quantity = fields.Float('Quantity', digits=0, help='Quantity', readonly=True)
    qty_end = fields.Float('Quantity End', digits=0, readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency', related='company_id.currency_id', readonly=True, required=True)
    price_unit = fields.Monetary('Unit Cost', readonly=True)
    price_total = fields.Monetary('Total Cost', readonly=True)
    standard_price = fields.Monetary('Standard Price', readonly=True)
    value_total = fields.Monetary('Total Value', readonly=True)
    stock_move_id = fields.Many2one('stock.move', 'Stock Move', readonly=True, check_company=True, index=True)
    account_move_id = fields.Many2one('account.move', 'Journal Entry', readonly=True, check_company=True)
