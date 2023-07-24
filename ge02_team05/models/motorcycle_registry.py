from odoo import fields, models


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"
    
    address = fields.Char(related="owner_id.contact_address_complete")
    country = fields.Char(related="owner_id.country_id.name")
