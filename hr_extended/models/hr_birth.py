from odoo import fields, models, api
from datetime import datetime, timedelta


class ModelName(models.Model):
    _inherit = 'hr.employee'

    def action_hr_birth(self):
        date = fields.Date.month()
        domain = [('birthday.month()', '=', date)]
        for line in self.search(domain):
            line.notification_account_move_line()

    def notification_account_move_line(self):
        self.env.ref("hr_extended.template_hr_birth").send_mail(self.id)
