# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    costs_hour_workcenter = fields.Float('Cost per hour worcenter', default=0.0)
    costs_hour_line = fields.Float('Cost per hour line', default=0.0)
    account_id = fields.Many2one('account.account', 'Account')
    line_ids = fields.One2many('mrp.workcenter.line', 'workcenter_id', 'Indirect costs')

    @api.model
    def create(self, vals):
        if vals.get('line_ids'):
            costs_hour_line = 0
            for lis in vals.get('line_ids'):
                dic = lis[2]
                costs_hour_line += dic.get('costs_hour')
            vals.update(costs_hour_line=costs_hour_line)
        return super(MrpWorkcenter, self).create(vals)

    def write(self, vals):
        res = super(MrpWorkcenter, self).write(vals)
        if vals.get('line_ids') or vals.get('costs_hour_workcenter') or vals.get('costs_hour_line') or 'costs_hour_line' in vals:
            for record in self:
                if vals.get('line_ids'):
                    costs_hour_line = 0
                    for line in record.line_ids:
                        costs_hour_line += line.costs_hour
                    record.write({'costs_hour_line': costs_hour_line})
                if vals.get('costs_hour_workcenter') or vals.get('costs_hour_line') or 'costs_hour_line' in vals:
                    costs_hour_workcenter = vals.get('costs_hour_workcenter') or record.costs_hour_workcenter
                    costs_hour_line = vals.get('costs_hour_line') or record.costs_hour_line
                    costs_hour = costs_hour_workcenter + costs_hour_line
                    record.write({'costs_hour': costs_hour})
        return res


class MrpWorkcenterLine(models.Model):
    _name = 'mrp.workcenter.line'
    _description = 'Work Center Line'

    workcenter_id = fields.Many2one('mrp.workcenter', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', 'Product', ondelete='set null')
    account_id = fields.Many2one('account.account', 'Account', ondelete='set null')
    costs_hour = fields.Float('Cost per hour', help='Specify cost per hour.', default=0.0)
