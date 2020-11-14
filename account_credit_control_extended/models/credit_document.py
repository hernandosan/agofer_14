# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountCreditDocument(models.Model):
    _name = 'credit.document'
    _description = 'Credit Document'

    type_id = fields.Many2one('credit.documents.type', 'Document Type', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')
    description = fields.Text('Description')
