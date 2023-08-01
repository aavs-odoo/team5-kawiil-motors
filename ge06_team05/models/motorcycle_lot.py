from odoo import api, fields, models
import re


class MotorycleLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def _get_next_serial(self, company, product):
        """Return the next serial number to be attributed to the product."""
        res = super()._get_next_serial(company, product)

        if product.tracking != "none" and product.product_tmpl_id.detailed_type == 'motorcycle':
            last_serial = self.env['stock.lot'].search(
                [('company_id', '=', company.id), ('product_id', '=', product.id)],
                limit=1, order='id DESC')
            if last_serial:
                pattern = '^[A-Z]{4}\d{2}[A-Z0-9]{2}\d{5}$'
                match = re.match(pattern, last_serial.name)
                if match:
                    return self.env['stock.lot'].generate_lot_names(last_serial.name, 2)[1]
                else:
                    return self.generate_format(product.product_tmpl_id)
            else:
                return self.generate_format(product.product_tmpl_id)

        return res

    def generate_format(self, lot_template):
        serial_template = lot_template.make + lot_template.model + str(lot_template.year) + lot_template.battery_capacity.upper()
        return serial_template + '00000'
