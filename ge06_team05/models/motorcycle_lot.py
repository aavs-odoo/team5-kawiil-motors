from odoo import api, fields, models
import re


class MotorycleLot(models.Model):
    _inherit = "stock.lot"

    @api.onchange('product_id')
    def _compute_serial_VIN(self):
        lot_registries = self.filtered(lambda r: r.product_id.product_tmpl_id.detailed_type == 'motorcycle')
        for lot in lot_registries:
            last_serial = self.env['stock.lot'].search(
                [('product_id', '=', lot.product_id.id)],
                limit=1, order='id DESC')
            if last_serial:
                pattern = '^[A-Z]{4}\d{2}[A-Z0-9]{2}\d{6}$'
                match = re.match(pattern, last_serial.name)
                if match:
                    lot.name = self.env['stock.lot'].generate_lot_names(last_serial.name, 2)[1]

                else:
                    lot.name = self.generate_format(lot.product_id.product_tmpl_id)

            else:
                lot.name = self.generate_format(lot.product_id.product_tmpl_id)

    # Genera el formato del numero serial a partir del VIN.
    # Toma los datos de make, model y year del template del producto seleccionado en el lot form.
    def generate_format(self, lot_template):
        serial_template = lot_template.make + lot_template.model + str(lot_template.year) + lot_template.battery_capacity.upper()
        return serial_template + '000000'