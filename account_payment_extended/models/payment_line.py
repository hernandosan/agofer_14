# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PaymentLine(models.Model):
    _name = 'payment.line'
    _rec_name = 'line_id'

    account_id = fields.Many2one('account.account', 'Account')

    amount = fields.Monetary('Amount', currency_field='currency_company_id')
    amount_currency = fields.Monetary('Currency Amount')
    amount_residual = fields.Monetary('Residual Amount', currency_field='currency_company_id')
    amount_residual_currency = fields.Monetary('Currency Residual Amount')

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    currency_id = fields.Many2one('res.currency', 'Currency')
    currency_company_id = fields.Many2one('res.currency', 'Company Currency')

    date = fields.Date('Date')
    date_maturity = fields.Date('Due Date')
    date_payment = fields.Date('Payment date')

    line_id = fields.Many2one('account.move.line', 'Line', required="True", ondelete="restrict")

    payment_id = fields.Many2one('account.payment', 'Payment', ondelete="cascade")
    payment_debit_id = fields.Many2one('account.payment', 'Debit Payment', ondelete="cascade")
    payment_credit_id = fields.Many2one('account.payment', 'Credit Payment', ondelete="cascade")

    total = fields.Monetary('Total', currency_field='currency_company_id', compute='_compute_total')
    total_currency = fields.Monetary('Currency Total')
    total_bool = fields.Boolean('Assign Total', default=False)

    @api.depends('currency_id', 'total_currency')
    def _compute_total(self):
        for line in self:
            line.total = line.currency_id._convert(line.total_currency, line.currency_company_id, line.company_id, line.date_payment)

    @api.onchange('total_bool')
    def _onchange_total_bool(self):
        if self.total_bool:
            self.total_currency = self.amount_residual_currency
