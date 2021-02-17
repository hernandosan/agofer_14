# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    order_id = fields.Many2one('sale.order', 'Order', copy=False, ondelete="cascade")

    @api.onchange('order_id')
    def _onchange_order_id(self):
        order_id = self.order_id
        destination_account_id = order_id.payment_account_id if order_id else self.destination_account_id
        journal_id = order_id.payment_journal_id if order_id else self.journal_id
        self.write({
            'destination_account_id': destination_account_id.id if destination_account_id else False,
            'journal_id': journal_id.id if journal_id else False,
        })

    def action_print_payment(self):
        return self.env.ref('account.action_report_payment_receipt').report_action(self)
