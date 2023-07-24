from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    is_new_customer = fields.Boolean(related="partner_id.is_new_customer")

    def setpricelist(self):
        for order in self:
            order.pricelist_id = self.env.ref('ge04_team05.list_new_customers_motorcycle')
            self.action_update_prices()
            order.is_new_customer = False
    
    def _get_update_prices_lines(self):
        return self.order_line.filtered(lambda line: line.product_type == "motorcycle")


