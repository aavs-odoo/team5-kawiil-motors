from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    is_new_customer = fields.Boolean(related="partner_id.is_new_customer")

    def setpricelist(self):
        for order in self:
            order.pricelist_id = 3
            order.action_update_prices()
