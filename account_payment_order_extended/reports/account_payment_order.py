# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    def report_bancolombia(self):
        self.ensure_one()
        tuple_string = (
            1,
            self.company_id.vat.zfill(10),
            self.company_id.name.ljust(16),
            self.order_type or 220,
            'Supplier'.ljust(10),
            str(self.date_done or fields.Date.today()).replace('-', ''),
            ' ',
            str(self.date_done or fields.Date.today()).replace('-', ''),
            str(len(self.payment_line_ids)).zfill(6),
            '0'.zfill(12),
            str(sum(line.amount_company_currency for line in self.payment_line_ids)),
            self.company_partner_bank_id.acc_number.zfill(11),
            'S'
        )
        string_control = '%s%s%s%s%s%s%s%s%s%s%s%s%s' % (tuple_string)

        string_detail = ''
        for line in self.payment_line_ids:
            tuple_string = (
                6,
                line.partner_id.ref_num.zfill(15),
                line.partner_id.name.ljust(18),
                line.partner_bank_id.bank_id.bic.zfill(9),
                line.partner_bank_id.acc_number.zfill(17),
                'S',
                27 if line.partner_bank_id.acc_type == 'saving' else 37,
                str(line.amount_company_currency).zfill(10),
                line.communication.ljust(9),
                (line.move_line_id.ref or '').ljust(12),
                ' '
            )
            string_format = '%s%s%s%s%s%s%s%s%s%s%s' % (tuple_string)
            string_detail += string_format + '\n'

        return string_control + '\n' + string_detail
