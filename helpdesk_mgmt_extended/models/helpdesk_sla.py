# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Helpdesksla(models.Model):
    _name = 'helpdesk.sla'
    _description = 'Helpdesk SLA'

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Name', required=True)
    team_id = fields.Many2one('helpdesk.ticket.team', 'Team')
    category_id = fields.Many2one('helpdesk.ticket.category', 'Category')
    type_id = fields.Many2one('helpdesk.ticket.type', 'Type')
    stage_id = fields.Many2one('helpdesk.ticket.stage', 'Stage')
    time_days = fields.Integer('Days')
    time_hours = fields.Integer('Hours')
    time_total = fields.Float('Time', compute='_compute_time_total', store=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    description = fields.Text('Description')
    priority = fields.Selection([('0','Low'),('1','Medium'),('2','High'),('3','Very High')], 'Priority', default='0') 

    @api.depends('time_days', 'time_hours')
    def _compute_time_total(self):
        for sla in self:
            sla.time_total = (sla.time_days * 24.0) + sla.time_hours
