# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    journal_id = fields.Many2one('account.journal', 'Journal', domain=[('type','in',('bank','cash'))])
