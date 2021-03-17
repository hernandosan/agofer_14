# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrBranch(models.Model):
    _name = 'hr.branch'
    _description = 'HR Branch'

    active = fields.Boolean('Active', default=True)
    biller_id = fields.Many2one('res.users', 'Biller')
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.user.company_id)
    cashier_id = fields.Many2one('res.users', 'Cashier')
    user_id = fields.Many2one('res.users', 'Director')
    name = fields.Char('Name', required=True)
    parent_id = fields.Many2one('hr.branch', 'Parent')
    partner_id = fields.Many2one('res.partner', 'Partner')
