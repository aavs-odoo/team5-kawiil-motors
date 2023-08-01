from odoo import api, fields, models


class LocationState(models.Model):
    _inherit = "res.country.state"

    warehouse_id = fields.Many2one(comodel_name="stock.warehouse")
    
class WarehouseSelection(models.Model):
    _inherit = 'sale.order'

    location_state = fields.Many2one("res.country.state", string="Select your State", ondelete='cascade', domain="[('country_id.id','=','233')]", default=False)
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse", related="location_state.warehouse_id")
    