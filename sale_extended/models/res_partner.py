# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one(default=lambda self: self.env.user)
    property_payment_term_id = fields.Many2one(default=lambda self: self.env.ref('account.account_payment_term_immediate'))

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.team_id = self.user_id.team_id if self.user_id else False

    def _partner_crossover_journal(self):
        self.ensure_one()
        if not self.team_id:
            raise ValidationError(_("The Partner %s has not CRM team") % self.name)
        return self.team_id._team_crossover_journal()
    
    def _partner_advance_journal(self):
        self.ensure_one()
        if not self.team_id:
            raise ValidationError(_("The Partner %s has not CRM team") % self.name)
        return self.team_id._team_advance_journal()
    
    def _partner_advance_account(self):
        self.ensure_one()
        if not self.team_id:
            raise ValidationError(_("The Partner %s has not CRM team") % self.name)
        return self.team_id._team_advance_account()
