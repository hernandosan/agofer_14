# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrDocument(models.Model):
    _name = 'hr.document'
    _description = 'HR Documents'

    type = fields.Selection([('0', 'HR'), ('1', 'SIG')])
    type_doc_id = fields.Many2one('hr.doc.type', 'Document Type')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')
    description = fields.Char('Description')
