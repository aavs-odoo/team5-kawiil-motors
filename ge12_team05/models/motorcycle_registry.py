from odoo import api, models
from odoo.exceptions import UserError


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    @api.model_create_multi
    def create(self, vals_list):
        registry = super().create(vals_list)
        if len(registry.env['res.users'].search([('name', 'like', registry.owner_id.name)])) == 0:
            users = registry.env['res.users'].create({
                'name': registry.owner_id.name,
                'login': registry.owner_email,
                'email': registry.owner_email
            })
            is_internal = users._is_internal()
            is_portal = False
            self.action_grant_access(users, is_internal, is_portal)

        return registry
     
    @api.depends('users')
    def action_grant_access(self, user, internal, portal):

        group_portal = self.env.ref('base.group_portal')
        group_user = self.env.ref('base.group_user')

        user_sudo = user.sudo()

        if not user_sudo.active or not portal:
            user_sudo.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_user.id)]})
            # prepare for the signup process
            user_sudo.partner_id.signup_prepare()

        self._send_email(user)

        return True
    
    def _send_email(self, user):
        user.ensure_one()
        template = self.env.ref('portal.mail_template_data_portal_welcome')
        if not template:
            raise UserError(('The template "Portal: new user" not found for sending email to the portal user.'))

        lang = user.sudo().lang
        partner = user.sudo().partner_id

        portal_url = partner.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[partner.id]
        partner.signup_prepare()

        template.with_context(dbname=self._cr.dbname, portal_url=portal_url, lang=lang).send_mail(self.id, force_send=True)

        return True
    
