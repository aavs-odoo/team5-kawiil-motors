from odoo import fields, models

class SaleOrder(models.Model):
    _inherit="sale.order"
    customer_type = fields.Boolean(related="partner_id.is_new_customer")