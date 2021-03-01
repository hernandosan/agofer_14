from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    plate = fields.Char('License Plate')
    type = fields.Selection(selection_add=[('driver', 'Driver')])
