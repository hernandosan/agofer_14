from odoo import fields, models, api


class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    communication = fields.Char(required=False)