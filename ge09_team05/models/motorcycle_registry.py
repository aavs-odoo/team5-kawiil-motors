from odoo import fields, models


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    repair_orders = fields.One2many(comodel_name="repair.order", inverse_name="registry_id", string="Repair Orders")

    def action_view_repair(self):
        return self._get_action_view_picking(self.repair_orders)

    def _get_action_view_picking(self, repair_orders):
        action = self.env["ir.actions.actions"]._for_xml_id("repair.action_repair_order_tree")

        if len(repair_orders) > 1:
            action['domain'] = [('id', 'in', repair_orders.ids)]
        elif repair_orders:
            form_view = [(self.env.ref('repair.view_repair_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = repair_orders.id
        return action