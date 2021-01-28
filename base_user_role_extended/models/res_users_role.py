# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsersRole(models.Model):
    _inherit = 'res.users.role'

    parent_id = fields.Many2one('res.users.role', 'Parent')
    child_id = fields.Many2one('res.users.role', 'Child')
