# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # def _default_property_payment_term_id(self):
    #     return self.env.ref('account.account_payment_term_immediate')

    user_id = fields.Many2one(default=lambda self: self.env.user)
    property_payment_term_id = fields.Many2one(default=lambda self: self.env.ref('account.account_payment_term_immediate'))

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.team_id = self.user_id.team_id if self.user_id else False