from odoo import http
from odoo.http import request


class SnippetControllers(http.Controller):
    @http.route(['/get_products'], type='json', auth='public', website=True)
    def get_products(self):
        motorcycles = http.request.env['motorcycle.registry'].search([])
        motorcycle_list = []
        for motorcycle in motorcycles:
            news = {
                "name": motorcycle.registry_number,
                "mileage": motorcycle.current_mileage,
                "vin": motorcycle.vin,
            }
            motorcycle_list.append(news)
        return motorcycle_list
