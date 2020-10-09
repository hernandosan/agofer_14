# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def action_account_move_line(self):
        date = fields.Date.today() - timedelta(days=30)
        domain = [('reconciled', '=', False), ('account_id.user_type_id', '=', 'receivable'),
                  ('date_maturity', '<=', date)]
        for line in self.search(domain):
            line.notification_account_move_line()

    def notification_account_move_line(self):
        self.env.ref("account_credit_control_extended.template_account_move_line").send_mail(self.id)
