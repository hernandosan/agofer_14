# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountGroup(models.Model):
    _inherit = 'account.group'

    niif_bool = fields.Boolean('Is NIIF', default=False, copy=False)
