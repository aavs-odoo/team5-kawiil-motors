from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('model', 'make', 'year')
    def _generate_name(self):
        product_registries = self.filtered(lambda r: r.detailed_type == 'motorcycle')
        for product in product_registries:
            product.make = product.make or '--'
            product.model = product.model or '--'
            product.name = str(product.make) + str(product.model) + str(product.year)
