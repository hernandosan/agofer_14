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
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)

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
        stock_move = self.env['stock.move'].sudo().search(domain, order='date desc', limit=1)
        standard_price = stock_move.standard_price or 0.0
        quantity = self.product_id.sudo().with_context(to_date=self.date_to, location=self.location_id.id).qty_available

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

        kardex_ids = []
        for move in moves:
            # Compute
            move_type = self._move_type(move)
            move_subtype = self._move_subtype(move, move_type)

            qty_done = - move.quantity_done if move_type == 'out' else move.quantity_done
            qty_init = quantity
            qty_out = qty_init + qty_done

            price_unit = move._get_price_unit()
            price_total = price_unit * qty_done

            # AVCO
            standard_price = move.standard_price
            quantity = qty_out
            standard_total = standard_price * quantity
            vals = {
                'stock_move_id': move.id,
                'stock_picking_id': move.picking_id.id if move.picking_id else False,
                'date': move.date,
                'product_id': move.product_id.id,
                'move_type': move_type,
                'move_subtype': move_subtype,
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

    def _move_type(self, move):
        # In, Out
        self.ensure_one()
        location = self.location_id.id
        origin = move.location_id.id
        destination = move.location_dest_id.id
        if location == destination:
            return 'in'
        elif location == origin:
            return 'out'
        else:
            return 'none'

    def _move_subtype(self, move, type):
        # Stock Location Usage
        self.ensure_one()
        origin = move.location_id
        destination = move.location_dest_id
        if type == 'in':
            return _(origin.usage)
        elif type == 'out':
            return _(destination.usage)
        else:
            return 'None'

    def action_view_kardex(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock_account_extended.action_stock_kardex_line")
        action['domain'] = [('kardex_id', '=', self.id)]
        return action


class StockKardexLine(models.Model):
    _name = 'stock.kardex.line'
    _description = 'Stock Kardex Line'
    _rec_name = 'product_id'

    account_move_id = fields.Many2one('account.move', 'Journal Entry', readonly=True, check_company=True)

    company_id = fields.Many2one('res.company', 'Company', related='kardex_id.company_id', readonly=True)

    currency_id = fields.Many2one('res.currency', 'Currency', related='company_id.currency_id', readonly=True, required=True)

    date = fields.Datetime('Date')

    location_id = fields.Many2one('stock.location', 'Source Location', check_company=True, help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.")
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', check_company=True, help="Location where the system will stock the finished products.")

    move_subtype = fields.Char('Subtype')
    move_type = fields.Char('Type')

    kardex_id = fields.Many2one('stock.kardex', 'Kardex', required=True, ondelete='cascade')

    price_total = fields.Monetary('Total Cost', readonly=True)
    price_unit = fields.Monetary('Unit Cost', readonly=True)

    product_id = fields.Many2one('product.product', 'Product', readonly=True, required=True, check_company=True)

    qty_end = fields.Float('Quantity End', digits=0, readonly=True)
    qty_init = fields.Float('Quantity Init', digits=0, readonly=True)
    quantity = fields.Float('Quantity', digits=0, help='Quantity', readonly=True)

    standard_price = fields.Monetary('Standard Price', readonly=True)

    stock_move_id = fields.Many2one('stock.move', 'Stock Move', readonly=True, check_company=True, index=True)
    stock_picking_id = fields.Many2one('stock.picking', 'Stock Picking', readonly=True, check_company=True, index=True)

    value_total = fields.Monetary('Total Value', readonly=True)

    user_id = fields.Many2one(related='kardex_id.user_id')
