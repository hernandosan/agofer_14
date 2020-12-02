from odoo import fields, models, api


class CreditCustomerWizard(models.Model):
    _name = 'credit.customer.wizard'
    _description = 'Credit Customer Wizard'

    partner_id = fields.Many2one('res.partner', 'Partner')


def action_credit_customer(self):
    print("Hi")


