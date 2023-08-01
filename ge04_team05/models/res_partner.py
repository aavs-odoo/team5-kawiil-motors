from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_new_customer = fields.Boolean(compute="_check_new_customer", default=True)

    def _check_new_customer(self):
        for partner in self:
            partner.is_new_customer = False
            if partner.sale_order_ids.order_line.filtered(lambda line: line.product_type == 'motorcycle'):
                partner.is_new_customer = False
            else:
                partner.is_new_customer = True
                
            if not partner.sale_order_ids:
                partner.is_new_customer = True
