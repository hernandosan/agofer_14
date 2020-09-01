# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tariff_code = fields.Char('Tariff Reference', compute='_compute_tariff_code', inverse='_set_tariff_code', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.tariff_code')
    def _compute_tariff_code(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.tariff_code = template.product_variant_ids.tariff_code
        for template in (self - unique_variants):
            template.tariff_code = False
    
    def _set_tariff_code(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.tariff_code = template.tariff_code


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tariff_code = fields.Char('Tariff Reference', index=True)
