# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    landed_costs_ids = fields.One2many('stock.landed.cost', 'order_id', 'Landed Costs')
    landed_costs_visible = fields.Boolean(compute='_compute_landed_costs_visible')

    @api.depends('order_line', 'order_line.is_landed_costs_line')
    def _compute_landed_costs_visible(self):
        for order in self:
            if order.landed_costs_ids:
                order.landed_costs_visible = False
            else:
                order.landed_costs_visible = any(line.is_landed_costs_line for line in order.order_line)

    def button_create_landed_costs(self):
        """Create a `stock.landed.cost` record associated to the account move of `self`, each
        `stock.landed.costs` lines mirroring the current `account.move.line` of self.
        """
        self.ensure_one()
        landed_costs_lines = self.order_line.filtered(lambda line: line.is_landed_costs_line)
        carrier_id = self.env['delivery.carrier'].search([('partner_id','=',self.partner_id.id)], limit=1)

        landed_costs = self.env['stock.landed.cost'].create({
            'order_id': self.id,
            'carrier_id': carrier_id.id if carrier_id else False,
            'cost_lines': [(0, 0, {
                'product_id': l.product_id.id,
                'name': l.product_id.name,
                'account_id': l.product_id.product_tmpl_id.get_product_accounts()['stock_input'].id,
                'price_unit': l.currency_id._convert(l.price_subtotal, l.order_id.company_id.currency_id, l.company_id, l.order_id.date_order),
                'split_method': 'equal',
            }) for l in landed_costs_lines],
        })
        action = self.env["ir.actions.actions"]._for_xml_id("stock_landed_costs.action_stock_landed_cost")
        return dict(action, view_mode='form', res_id=landed_costs.id, views=[(False, 'form')])

    def action_view_landed_costs(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock_landed_costs.action_stock_landed_cost")
        domain = [('id', 'in', self.landed_costs_ids.ids)]
        context = dict(self.env.context, default_vendor_bill_id=self.id)
        views = [(self.env.ref('stock_landed_costs.view_stock_landed_cost_tree2').id, 'tree'), (False, 'form'), (False, 'kanban')]
        return dict(action, domain=domain, context=context, views=views)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_type = fields.Selection(related='product_id.type', readonly=True)
    is_landed_costs_line = fields.Boolean()

    @api.onchange('product_id')
    def _onchange_is_landed_costs_line_product(self):
        if self.product_id.landed_cost_ok:
            self.is_landed_costs_line = True
        else:
            self.is_landed_costs_line = False
