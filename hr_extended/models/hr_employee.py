# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import calendar


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    document_ids = fields.One2many('hr.document', 'employee_id', 'Documents')

    def action_hr_birth(self):
        month = fields.Date.today().month
        employees = self.search([('birthday', '!=', False)])
        ids = [employee.id for employee in employees if employee.birthday.month == month]
        if ids:
            self.notification_hr_birth()

    def action_hr_birth_post(self):
        employees = self.search([('birthday', '!=', False)])
        ids = [employee.id for employee in employees if employee.birthday == fields.Date.today()]
        self.post_hr_birth(ids)

    def mail_hr_birth(self):
        users = self.env.ref('hr.group_hr_manager').users
        partners = users.partner_id
        mails = ''
        for partner in partners:
            mails += partner.email + ', '
        return mails

    def month_hr_birth(self):
        return _(calendar.month_name[fields.Date.today().month]).capitalize()

    def lang_hr_birth(self):
        return self.env.user.lang

    def notification_hr_birth(self):
        self.env.ref("hr_extended.template_hr_birth").send_mail(self.env.ref('hr.employee_admin').id)

    def post_hr_birth(self, ids):
        for id in ids:
            self.env.ref("hr_extended.template_hr_birth_post").send_mail(id)

    def table_hr_birth(self):
        month = fields.Date.today().month
        employees = self.search([('birthday', '!=', False)])
        ids = [employee.id for employee in employees if employee.birthday.month == month]
        table_hr_birth = ""
        if ids:
            table_hr_birth += """
            <table style="border: 1px solid black">
            <thead>
                <tr>
                    <th style="border: 1px solid black"> """ + _('Employee') + """ </th>
                    <th style="border: 1px solid black"> """ + _('Birthday') + """ </th>
                </tr>
            </thead>
            <tbody>
            """
        for employee in self.browse(ids):
            table_hr_birth += "<tr>" + '<td style="border: 1px solid black">' + employee.name + "</td>" \
                              + '<td style="border: 1px solid black">' + employee.birthday.strftime('%d/%m/%Y') \
                              + "</td>" + "</tr>"
        if ids:
            table_hr_birth += "</tbody>" + "</table>"
        return table_hr_birth
