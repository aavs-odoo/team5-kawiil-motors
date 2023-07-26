from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_new_customer = fields.Boolean(compute="_check_new_customer", default=True)

    def _check_new_customer(self):
        for record in self:
            record.is_new_customer=False
            for order in record.sale_order_ids.order_line:
                if order.product_type != "motorcycle":
                    record.is_new_customer=True
                else:
                    record.is_new_customer=False
                    break
            if not record.sale_order_ids:
                record.is_new_customer = True
