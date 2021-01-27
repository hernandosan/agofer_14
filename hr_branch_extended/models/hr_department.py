# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    branch_id = fields.Many2one('hr.branch', 'Branch')
