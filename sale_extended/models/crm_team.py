# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    crossover_journal_id = fields.Many2one('account.journal', 'Crossover Journal', domain=[('type','in',('bank','cash'))])
    advance_journal_id = fields.Many2one('account.journal', 'Advance Journal', domain=[('type','in',('bank','cash'))])
    advance_account_id = fields.Many2one('account.account', 'Advance Account', domain=[('user_type_id.type','=','payable')])

    def _team_crossover_journal(self):
        self.ensure_one()
        if not self.crossover_journal_id:
            raise ValidationError(_("The CRM Team %s has not crossover journal") % self.name)
        return self.crossover_journal_id
    
    def _team_advance_journal(self):
        self.ensure_one()
        if not self.advance_journal_id:
            raise ValidationError(_("The CRM Team %s has not advance journal") % self.name)
        return self.crossover_journal_id
    
    def _team_advance_account(self):
        self.ensure_one()
        if not self.advance_account_id:
            raise ValidationError(_("The CRM Team %s has not advance account") % self.name)
        return self.advance_account_id
