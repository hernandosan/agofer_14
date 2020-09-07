# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tariff_code = fields.Char('Tariff Reference', compute='_compute_tariff_code', inverse='_set_tariff_code', store=True)
    tariff_ids = fields.One2many('product.tariff', 'template_id', 'Tariff', compute='_compute_tariff_ids', inverse='_set_tariff_ids', store=True)

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

    @api.depends('product_variant_ids', 'product_variant_ids.tariff_ids')
    def _compute_tariff_ids(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.tariff_ids = template.product_variant_ids.tariff_ids
        for template in (self - unique_variants):
            template.tariff_ids = False

    def _set_tariff_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.tariff_ids = template.tariff_ids


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tariff_code = fields.Char('Tariff Reference', index=True)
    tariff_ids = fields.One2many('product.tariff', 'product_id', 'Tariff')


class ProductTariff(models.Model):
    _name = 'product.tariff'
    _description = 'Product tariff'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    template_id = fields.Many2one('product.template', 'Template', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', ondelete='cascade')
    country_id = fields.Many2one('res.country', 'Country', ondelete='cascade')
    tax_id = fields.Many2one('account.tax', 'Tax', ondelete='cascade')
