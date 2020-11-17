# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def action_account_move_line(self):
        date = fields.Date.today() - timedelta(days=30)
        domain = [
            ('account_id.user_type_id', '=', 'receivable'), 
            ('reconciled', '!=', True), 
            ('date_maturity', '<=', date), 
            ('partner_id', '!=', False), 
            ('partner_id.user_id', '!=', False)
        ]
        for line in self.search(domain):
            line._notification_account_move_line()

    def _notification_account_move_line(self):
        self.ensure_one()
        self.env.ref("account_credit_control_extended.template_account_move_line").send_mail(self.id)
