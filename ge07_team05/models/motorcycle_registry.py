from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    license_plate = fields.Char(string='License Plate Number', default="XXX000")
    current_mileage = fields.Float(string='Current Mileage', default=1000.0)

    lot_ids = fields.One2many(comodel_name="stock.lot", inverse_name="registry_id", string="Motorcycle Lot Number")
    lot_id = fields.Many2one(comodel_name="stock.lot", string="Lot Number", compute="_compute_lot_id")

    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    owner_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict', related="sale_id.partner_id")

    @api.constrains('lot_ids')
    def _constains_stock_lot_ids(self):
        for registry in self:
            registered_stock_lots = registry.lot_ids

            if len(registered_stock_lots) > 1:
                raise ValidationError(_('Odoopsie! Only one Lot is allowed per registry.'))

    @api.depends('lot_ids')
    def _compute_lot_id(self):
        for registry in self:
            registry.lot_id = registry.lot_ids.id if registry.lot_ids else False
