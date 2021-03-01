# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    order_type = fields.Selection([('220', 'Supplier'), ('225', 'Payroll')], 'Order Type')

    def generate_payment_file(self):
        if self.payment_method_id.code == "electronic":
            report = self.company_partner_bank_id.bank_id.report_id
            report_service = report.report_name

            if report.report_type in ['qweb-html', 'qweb-pdf']:
                result, format = report._render_qweb_pdf([self.id])
            else:
                res = report._render([self.id])
                if not res:
                    raise UserError(_('Unsupported report type %s found.', report.report_type))
                result, format = res

            report_name = 'report.' + report_service
            ext = "." + format
            if not report_name.endswith(ext):
                report_name += ext

            return (result, report_name)
        else:
            return super(AccountPaymentOrder, self).generate_payment_file()
