from odoo import fields, models, api, _
from odoo.odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    payment_date = fields.Date('Payment Date', required=True)
    order_type = fields.Selection([('220', 'Supplier'), ('225', 'Payroll')], 'Order Type')

    def generate_payment_file(self):
        if self.payment_method_id.code == "electronic":
            report = self.company_partner_bank_id.bank_id.report_id

            res = report._render([self.id])
            if not res:
                raise UserError(_('Unsupported report type %s found.', report.report_type))
            result, format = res

            report_name = self.name.lower()
            ext = "." + 'txt'
            report_name += ext

            return (result, report_name)
        else:
            return super(AccountPaymentOrder, self).generate_payment_file()

    def _prepare_move_line_partner_account(self, bank_line):
        vals = super(AccountPaymentOrder, self)._prepare_move_line_partner_account(bank_line)
        vals.update(date=self.payment_date)
        return vals
