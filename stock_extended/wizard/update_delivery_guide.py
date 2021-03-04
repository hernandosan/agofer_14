from odoo import fields, models, api


class UpdateDeliveryGuide(models.Model):
    _name = 'update.delivery.guide'
    _description = 'Update Delivery Guide'

    def _default_guides_ids(self):
        return self.env['delivery.guide'].browse(self._context.get('active_ids'))

    guides_ids = fields.Many2many('delivery.guide', string='Delivery guides', default=_default_guides_ids)

    def update_delivery(self):
        self.guides_ids.filtered(lambda g: g.state == 'confirm').action_delivered()
