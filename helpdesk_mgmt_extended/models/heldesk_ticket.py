# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    type_id = fields.Many2one('helpdesk.ticket.type', 'Type')
    sla_id = fields.Many2one('helpdesk.sla', 'SLA')
    time_hours = fields.Float('ANS')
    timesheet = fields.Datetime('Deadline')
    expiration = fields.Integer(compute="_compute_progress", string='Expiration')
    duration = fields.Float('Duration', help='Duration in hours')
    sla_date = fields.Datetime('SLA_Deadline')

    @api.model
    def create(self, vals):
        category_id = self.env['helpdesk.ticket.category'].sudo().browse(int(vals.get('category_id')))
        team_id = category_id.team_id
        user_id = team_id.alias_user_id
        domain = [('category_id','=',category_id.id),('team_id','=',team_id.id)]
        sla_id = self.env['helpdesk.sla'].sudo().search(domain)
        vals.update(team_id=team_id.id, user_id=user_id.id, sla_id=sla_id.id, time_hours=sla_id.time_total,
                    timesheet=fields.Datetime.from_string(fields.Datetime.now()) + relativedelta(hours=sla_id.time_total))
        return super(HelpdeskTicket, self).create(vals)

    def _compute_progress(self):
        for ticket in self:
            t1 = datetime.strptime(str(ticket.create_date), '%Y-%m-%d %H:%M:%S.%f')
            t2 = datetime.strptime(str(fields.Datetime.now()), '%Y-%m-%d %H:%M:%S')
            t3 = abs(t2 - t1)
            hours = ((round(t3.seconds/60))/60)
            time = (hours/ticket.time_hours)*100
            if time == 100:
                ticket.expiration = 100
            else:
                ticket.expiration = time
        return ticket.expiration