from odoo import api, fields, models


# en esta clase aplicar la herencia de create_serial_number
class MotorcycleProduction(models.Model):
    _inherit = "mrp.production"
