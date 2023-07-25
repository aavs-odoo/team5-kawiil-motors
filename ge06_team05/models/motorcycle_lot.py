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
                    lot_template = lot.product_id.product_tmpl_id
                    serial_template = lot_template.make + lot_template.model + str(lot_template.year) + lot_template.battery_capacity.upper()
                    lot.name = serial_template + '000000'
            else:
                lot_template = lot.product_id.product_tmpl_id
                serial_template = lot_template.make + lot_template.model + str(lot_template.year) + lot_template.battery_capacity.upper()
                lot.name = serial_template + '000000'

    """
            if last_serial:
                pattern = '^[A-Z]{4}\d{2}[A-Z0-9]{2}\d{5}$'
                match = re.match(pattern, last_serial.name)
                if not match:
                    lot_template = lot.product_id.product_tmpl_id
                    serial_template = lot_template.make + lot_template.model + str(lot_template.year) + lot_template.battery_capacity.upper()
                    lot.name = serial_template + '000000'
                else:
                    lot.name = self.env['stock.lot'].generate_lot_names(last_serial.name, 2)[1]
            else:
                lot_template = lot.product_id.product_tmpl_id
                serial_template = lot_template.make + lot_template.model + str(lot_template.year) + lot_template.battery_capacity.upper()
                lot.name = serial_template + '000000'
    """

    # name es el Lot/Serial Number


    # product_id.product_tmpl_id.detailed_type == 'motorcycle,':
    # product_id apunta al product_template que pertenece. Por eso desde ahi es que se puede extraer el detailed_type
    

    # pasos:
    # generar el VIN desde las propiedades de la moto (excluyendo serial number)
    # generar el serial number automatico (puede ser por la funcionalidad de stock.lot) (aca esta lo dificil)
    # asignar el nuevo VIN al manufacturing order
