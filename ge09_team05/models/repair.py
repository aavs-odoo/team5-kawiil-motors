from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit='repair.order'

    vin = fields.Char(string='VIN', required=True)
    mileage = fields.Char(string='Mileage')
    registry_id = fields.Many2one(compute="_get_registry_from_vin", comodel_name="motorcycle.registry")
    partner_id = fields.Many2one(related="registry_id.owner_id", string="Owner")
    sale_order_id = fields.Many2one(related="registry_id.sale_id", string="Sales")
    product_id = fields.Many2one(related="registry_id.lot_id.product_id", string="Products", required=False)
    lot_id = fields.Many2one(related="registry_id.lot_id")

    @api.depends('vin')
    def _get_registry_from_vin(self):
        for repair_order in self:
            motorcycle = self.env['motorcycle.registry'].search([('vin', '=', repair_order.vin)])
            repair_order.registry_id = motorcycle if motorcycle else False
