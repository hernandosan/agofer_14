# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskCategoryTeam(models.Model):
    _inherit = "helpdesk.ticket.category"

    team_id = fields.Many2one('helpdesk.ticket.team','Team')