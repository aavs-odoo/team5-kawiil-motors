# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class CustomerPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        RepairOrder = request.env['repair.order']
        if 'orders_count' in counters:
            values['orders_count'] = RepairOrder.search_count(self._prepare_repair_orders_domain()) \
            if RepairOrder.check_access_rights('read', raise_exception=False) else 0
        return values

    def _prepare_repair_orders_search_domain(self, repair_order_search):
        domain = []
        default_domain = self._prepare_repair_orders_domain()
        searchable_fields = {
            'name': ('name', '=ilike', repair_order_search['name']),
            'vin': ('vin', '=ilike', repair_order_search['vin']),
            }  
        for key in list(repair_order_search):
            if repair_order_search[key] != '':
                domain.append(searchable_fields[key])
        return domain + default_domain

    def _prepare_repair_orders_domain(self):
        return [
            ('state', 'in', ['draft', 'confirmed', 'ready', 'under-repair', 'done'])
        ]

    def _get_repair_orders_searchbar_sortings(self):
        return {
            'date': {'label': _('Order Date'), 'order': 'create_date desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'vin': {'label': _('VIN'), 'order': 'vin asc, name desc'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }
    
    def _prepare_repair_order_portal_rendering_values(
        self, page=1, date_begin = None, date_end = None, sortby = None, orders_page = False, **kwargs
    ):
        values = self._prepare_portal_layout_values()
        RepairOrder = request.env['repair.order']
        if not sortby:
            sortby = 'date'

        search_parameters = ['name', 'vin']

        args = list(kwargs)
        to_search = set(args) & set(search_parameters)
        if len(to_search) > 0:
            url = "my/repair_order/"
            domain = self._prepare_repair_orders_search_domain(kwargs)
        else:
            url = "/my/repair_orders/"
            domain = self._prepare_repair_orders_domain()


        searchbar_sortings = self._get_repair_orders_searchbar_sortings()
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        pager_values = portal_pager(
            url = url,
            total = RepairOrder.search_count(domain),
            page = page,
            step = self._items_per_page,
            url_args = {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
        )
        orders = RepairOrder.search(domain, order = sort_order, limit = self._items_per_page, offset=pager_values['offset'])
        values.update({
            'date': date_begin,
            'repair_orders': orders.sudo() if orders_page else RepairOrder,
            'page_name': 'Orders Page' if orders_page else 'Repair Order',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return values

    @http.route(['/my/repair_order/', '/my/repair_order/page/<int:page>'], type = 'http', auth = "user", website = True)
    def portal_my_repair_order(self, **kwargs):
        values = self._prepare_repair_order_portal_rendering_values(orders_page = True, **kwargs)
        return request.render("ge11_team05.portal_my_repair_order", values)

    @http.route(['/my/repair_order/<int:repair_order_id>'], type = 'http', auth = "public", website = True)
    def repair_order_page(self, repair_order_id, access_token = None, **kw):
        try:
            repair_order_sudo = self._document_check_access('repair.order', repair_order_id, access_token = access_token)
        except (AccessError, MissingError):
            return request.redirect('/my/')
        
        backend_url = f'/web#model={repair_order_sudo._name}'\
                      f'&id={repair_order_sudo.id}'\
                      f'&action={repair_order_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'repair_order': repair_order_sudo,
            'backend_url': backend_url,
            'res_company': repair_order_sudo.partner_id,
        }
        return request.render('ge11_team05.repair_order_portal_template', values)

    @http.route(["/my/repair_orders/"], type = 'http', auth = "user", website = True)
    def portal_my_repair_orders(self, **kwargs):
        values = self._prepare_repair_order_portal_rendering_values(orders_page = True, **kwargs)
        return request.render("ge11_team05.portal_my_repair_orders", values)
    
    @http.route(['/my/generate_repair_orders/'], type = 'http', auth = "public", website = True)
    def _repair_order_post(self, **post):
        if post and request.httprequest.method == 'POST':
            try:
                repair_order = request.env['repair.order']
                repair_order.create({'vin': post['vin'], 'mileage': post['mileage']})
            except(AccessError, MissingError):
                return request.redirect('/my/')
        return request.redirect('/my/repair_order/')
    
    @http.route(['/my/generate_repair_order/'], type = 'http', auth = "user", website = True)
    def generate_repair_order(self, **kwargs):
        values = self._prepare_repair_order_portal_rendering_values(orders_page = False, **kwargs)
        return request.render("ge11_team05.generate_repair_order_portal_template", values)
    
    @http.route(['/my/search_repair_orders/'], type = 'http', auth = "user", website = True)
    def search_repair_orders(self, **kwargs):
        return request.render('ge11_team05.repair_orders_search_portal_template')