# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskCategoryTeam(models.Model):
    _inherit = "helpdesk.ticket.team"

    category_ids = fields.One2many('helpdesk.ticket.catagory', 'team_id', 'Categories')
