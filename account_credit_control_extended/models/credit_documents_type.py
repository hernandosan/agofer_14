# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreditDocumentType(models.Model):
    _name = 'credit.documents.type'
    _description = 'Credit Documents Type'

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Document Type', required=True)
