# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    crossover_journal_id = fields.Many2one('account.journal', 'Crossover Journal', domain=[('type','in',('bank','cash'))])
    advance_journal_id = fields.Many2one('account.journal', 'Advance Journal', domain=[('type','in',('bank','cash'))])
    advance_account_id = fields.Many2one('account.account', 'Advance Account', domain=[('user_type_id.type','=','payable')])
