# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskTicketType(models.Model):
    _name = 'helpdesk.ticket.type'
    _description = 'Helpdesk Ticket Type'
    _order = "sequence, id"

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
