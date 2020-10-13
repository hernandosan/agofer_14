# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrDocumentType(models.Model):
    _inherit = 'hr.employee'

    document_id = fields.One2many('hr.document', 'employee_id', 'Documents')

