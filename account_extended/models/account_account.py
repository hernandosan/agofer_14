# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    niif_group_id = fields.Many2one('account.group', 'NIIF Group', domain=[('niif_bool','=',True)], copy=False)
