from odoo import models


class RepairOrder(models.Model):
    _name = 'repair.order'
    _inherit = ['repair.order', 'portal.mixin']
    
    def _compute_access_url(self):
        super()._compute_access_url()
        for repair_order in self:
            repair_order.access_url = f'/my/repair_order/{repair_order.id}'
    
    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('ge11_team05.portal_my_repair_order')
