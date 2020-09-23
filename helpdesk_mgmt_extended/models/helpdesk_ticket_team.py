# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicketTeam(models.Model):
    _inherit = "helpdesk.ticket.team"

    category_ids = fields.One2many('helpdesk.ticket.category', 'team_id', 'Categories')
