# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DeliveryInvoice(models.Model):
    _name = 'delivery.invoice'
    _description = 'Delivery Invoice'
    _order = 'id desc'
    _rec_name = 'move_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    guides_ids = fields.Many2many('delivery.guide', string='Guides')
    journal_id = fields.Many2one('account.journal', 'Journal')
    move_id = fields.Many2one('account.move', 'Invoice')
    notes = fields.Text('Notes')
    partner_id = fields.Many2one('res.partner', 'Carrier')
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Cancel')], 'state', required=True, default='draft')
    user_id = fields.Many2one('res.user', 'User', default=lambda self: self.env.user)
    weight = fields.Float('Weight')
    weight_returned = fields.Float('Weight Returned')

    def action_confirm(self):
        self.write({'state': 'done'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
