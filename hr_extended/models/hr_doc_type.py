# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrDocumentType(models.Model):
    _name = 'hr.doc.type'
    _description = 'HR Documents Type'

    active = fields.Boolean(string='Active', trim=True)
    name = fields.Char('Document Type')
