# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    type_id = fields.Many2one('helpdesk.ticket.type', 'Type')
    sla_id = fields.Many2one('helpdesk.sla', 'SLA')
    sla_time = fields.Float('SLA Time')
    sla_deadline = fields.Datetime('SLA Deadline')
    sla_date = fields.Datetime('SLA Date', copy=False)
    sla_progress = fields.Float('SLA Progress', compute='_compute_sla_progress')

    @api.model
    def create(self, vals):
        category_id = self.env['helpdesk.ticket.category'].sudo().browse(int(vals.get('category_id')))
        team_id = category_id.team_id
        user_id = team_id.alias_user_id
        domain = [('category_id','=',category_id.id),('team_id','=',team_id.id)]
        sla_id = self.env['helpdesk.sla'].sudo().search(domain)
        vals.update(team_id=team_id.id, user_id=user_id.id, sla_id=sla_id.id, 
                    sla_time=sla_id.time_total, sla_deadline=fields.Datetime.now() + timedelta(hours=sla_id.time_total))
        return super(HelpdeskTicket, self).create(vals)

    def write(self, vals):
        if vals.get('stage_id') and vals.get('stage_id') == self.env.ref('helpdesk_mgmt_extended.helpdesk_ticket_stage_result').id:
            vals.update({'sla_date': fields.Datetime.now()})
        return super(HelpdeskTicket, self).write(vals)

    @api.depends('sla_date')
    def _compute_sla_progress(self):
        for ticket in self:
            datetime = fields.Datetime.now()
            time = (ticket.sla_date or datetime) - (ticket.create_date or datetime)
            progress = time.seconds / 3600
            ticket.update({'sla_progress': progress})
