# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreditDocument(models.Model):
    _name = 'credit.document'
    _description = 'Credit Document'
    _order = 'id desc'

    type_id = fields.Many2one('credit.document.type', 'Document Type', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    file_data = fields.Binary('File', attachment=True)
    file_name = fields.Char('File Name')
    description = fields.Text('Description')


class CreditDocumentType(models.Model):
    _name = 'credit.document.type'
    _description = 'Credit Documents Type'

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Document Type', required=True)
