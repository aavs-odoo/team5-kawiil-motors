# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class SnippetControllers(http.Controller):
    @http.route(['/get_products'], type='json', auth='public', website=True)
    def get_products(self):
        motorcycles = http.request.env['motorcycle.registry'].search([])
        motos = []
        for motorcycle in motorcycles:
            news = {
                "name": motorcycle.registry_number,
                "mileage": motorcycle.current_mileage,
                "vin": motorcycle.vin,
            }
            motos.append(news)
        return motos
