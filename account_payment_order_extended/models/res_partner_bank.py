from odoo import fields, models, api


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    acc_type = fields.Selection([('saving', 'Saving'), ('current', 'Current')], default='saving', compute=False)
