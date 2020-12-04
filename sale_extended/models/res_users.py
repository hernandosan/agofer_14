# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = 'res.users'

    teams_ids = fields.Many2many('crm.team', 'team_user_rel', 'user_id', 'team_id', 'Members', check_company=True)

    def _teams_ids(self):
        self.ensure_one()
        return self.teams_ids
