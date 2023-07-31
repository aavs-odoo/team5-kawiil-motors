from odoo import fields, http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import pager as portal_pager


class CurstomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        MotorcycleRegistry = request.env['motorcycle.registry']
        if 'registry_count' in counters:
            values['registry_count'] = MotorcycleRegistry.search_count(self._prepare_motorcycle_registries_domain(partner)) \
                if MotorcycleRegistry.check_access_rights('read', raise_exception=False) else 0

        return values
        
    def _prepare_motorcycle_registries_domain(self, partner):
        print("domain original",partner.id)
        return ['|',('is_public','=',True),('owner_id','child_of',partner.id)]

    def _prepare_motorcycle_search_domain(self, partner, registry_search):      
        domain = []

        searchable_fields = {
            'name': ('owner_id.name', 'like', registry_search['name']),
            'state': ('owner_id.state_id.name', 'like', registry_search['state']),
            'country': ('owner_id.country_id.name', 'like', registry_search['country']),
            'make': ('make', '=ilike', registry_search['make']),
            'model': ('model', '=ilike', registry_search['model']),
            }
        
        for key in registry_search:
            if key in list(searchable_fields):
                domain.append(searchable_fields[key])

        return domain + self._prepare_motorcycle_registries_domain(partner)

    def _prepare_registry_domain(self, partner):
        return [
            '|',('is_public','=',True),('owner_id','=','partner'),
        ]

    def _get_motorcycle_registries_searchbar_sortings(self):
        return {
            'date': {'label': _('Registry Date'), 'order': 'date_order desc'},
            'number': {'label': _('Registry Number'), 'order': 'registry_number'},
            'vin': {'label': _('VIN'), 'order': 'vin'},
        }

    def _prepare_motorcycle_registry_portal_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, motorcycle_registries_page=False, **kwargs
    ):
        MotorcycleRegistry = request.env['motorcycle.registry']

        if not sortby:
            sortby = 'number'

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()
        
        search_parameters = ['name', 'state', 'country', 'make', 'model']
        url = "my/motorcycle_registries"

        """ Revisa que en kwargs se tenga almenos un key que haga match con algun parametro
         antes de llamar la función del filtro personalizado
        """
        args = list(kwargs)
        to_search = set(args) & set(search_parameters)
        if len(to_search) > 0: 
            domain = self._prepare_motorcycle_search_domain(partner, kwargs)
        else:
            domain = self._prepare_motorcycle_registries_domain(partner)

        searchbar_sortings = self._get_motorcycle_registries_searchbar_sortings()

        sort_order = searchbar_sortings[sortby]['order']

        pager_values = portal_pager(
            url=url,
            total=MotorcycleRegistry.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={}
        )
        registries = MotorcycleRegistry.search(domain, order=sort_order, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'date': date_begin,
            'registries': registries.sudo() if motorcycle_registries_page else MotorcycleRegistry,
            'page_name': 'motorcycle_registries' if motorcycle_registries_page else 'registry',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        return values

    @http.route(['/my/motorcycle_registries', '/my/motorcycle_registries/page/<int:page>'], type='http', auth="user", 
    website=True)
    def portal_my_registries(self, **kwargs):
        values = self._prepare_motorcycle_registry_portal_rendering_values(motorcycle_registries_page=True, **kwargs)
        #request.session['my_quotations_history'] = values['registries'].ids[:100]
        return request.render("ge08_team05.portal_my_registries", values)

    @http.route(['/my/registry/<int:registry_id>'], type='http', auth="public", website=True)
    def registry_page(self, registry_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            registry_sudo = self._document_check_access('motorcycle.registry', registry_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_registry_%s' % registry_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_registry_%s' % registry_sudo.id] = today
                # The "Quotation viewed by customer" log note is an information
                # dedicated to the salesman and shouldn't be translated in the customer/website lgg
                context = {'lang': registry_sudo.user_id.partner_id.lang or registry_sudo.company_id.partner_id.lang}
                msg = _('Quotation viewed by customer %s', registry_sudo.partner_id.name if request.env.user._is_public() else request.env.user.partner_id.name)
                del context
                _message_post_helper(
                    "motorcycle.registry",
                    registry_sudo.id,
                    message=msg,
                    token=registry_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=registry_sudo.user_id.sudo().partner_id.ids,
                )

        backend_url = f'/web#model={registry_sudo._name}'\
                      f'&id={registry_sudo.id}'\
                      f'&action={registry_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'registry': registry_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': registry_sudo.owner_id,
        }
        
        return request.render('ge08_team05.registry_portal_template', values)
        
    # Ruta fantasma para recibir el POST
    @http.route(['/my/registry/change_registry'], type='http', auth="public", website=True)
    def registry_edit_page(self, report_type=None, access_token=None, message=False, download=False, **post):
        if post and request.httprequest.method == 'POST':
            try:
                if 'check_public' not in post:
                    post['check_public'] = False
                registry_sudo = request.env['motorcycle.registry'].browse(post['registry_id'])
                registry_sudo.write({
                    'license_plate':post['new_license'],
                    'current_mileage':post['new_mileage'],
                    'is_public':post['check_public']
                    })  

            except (AccessError, MissingError):
                return request.redirect('/my')
        
        # Independientemente de si recibe un post o no, redirige a la lista
        return request.redirect('/my/motorcycle_registries')
        
    @http.route(['/my/search_registries'], type='http', auth="public", website=True)
    def registry_search_page(self, report_type=None, access_token=None, message=False, download=False, **post):
        return request.render('ge08_team05.registry_search_portal_template')
