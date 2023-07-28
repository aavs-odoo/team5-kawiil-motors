from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super()._action_done()
        
        pickings = self.filtered(lambda p: (p.state == 'done' and p.product_id.product_tmpl_id.detailed_type == 'motorcycle')) #filtro 
        for picking in pickings:
            related_sale = picking.sale_id
            generated_lot = related_sale.mrp_production_ids.lot_producing_id
            self.env['motorcycle.registry'].create({'lot_ids': generated_lot, 'sale_id': related_sale.id, 'vin': generated_lot.name})

        return res
