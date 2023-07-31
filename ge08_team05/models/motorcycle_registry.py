from odoo import api, fields, models


class MotorcycleRegistry(models.Model):
    _name = 'motorcycle.registry'
    _inherit = ['motorcycle.registry', 'portal.mixin']

    is_public = fields.Boolean(string="Public Profile", default=False)

    def _compute_access_url(self):
        super()._compute_access_url()
        for registry in self:
            registry.access_url = f'/my/registry/{registry.id}'

    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('ge08_team05.portal_my_registry')
