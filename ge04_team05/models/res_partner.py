from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_new_customer = fields.Boolean(compute="_check_new_customer", default=True)

    def _check_new_customer(self):
        # usar partner es mas descriptivo en lugar de record
        for record in self:
            # cuando asignamos variables en python ponemos especio normalmente entre = 
            record.is_new_customer=False
            # if partner.sale_order_ids.order_line.filtered(lamdba line: line.product_type == 'motorcycle'):
            #     partner.is_new_customer = False
            # else:
            #     partner.is_new_customer = True
            for order in record.sale_order_ids.order_line:
                if order.product_type != "motorcycle":
                    record.is_new_customer=True
                else:
                    record.is_new_customer=False
                    break
            if not record.sale_order_ids:
                record.is_new_customer = True
# recuerda quitar el codigo comentado 

'''

_inherit = "sale.order"

    is_new_customer = fields.Boolean(compute="_check_new_customer", default=True)

    def _check_new_customer(self):
        for record in self:
            record.is_new_customer=False
            for order in record.order_line:
                if order.product_type != "motorcycle":
                    record.is_new_customer=True
                else:
                    record.is_new_customer=False
                    break
            if not record:
                record.is_new_customer = True

'''

