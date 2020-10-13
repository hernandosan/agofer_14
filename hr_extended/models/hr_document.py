# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrDocument(models.Model):
    _name = 'hr.document'
    _description = 'HR Documents'

    type = fields.Selection([('hr', 'HR'), ('sig', 'SIG')], required=True)
    type_id = fields.Many2one('hr.doc.type', 'Document Type', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')
    description = fields.Text('Description')
