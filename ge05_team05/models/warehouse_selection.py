from odoo import api, fields, models

class WarehouseSelection(models.Model):
    _inherit = 'sale.order'
    
    warehouse_dic={'NY':3,'PA':3,'ME':3,'VT':3,'NH':3,'MA':3,'CT':3,'RI':3,'NJ':3,'DE':3,'MD':3,'VA':3,'WV':3,'OH':3,'NC':3,
                   'SC':3,'KY':3,'TN':3,'GA':3,'FL':3,'MI':3,'IN':3,'AL':3,'MS':3,'IL':3,'WI':3,'MN':3,'IA':3,'MO':3,'AR':3,
                   'LA':3,'DF':1,'CA':4,'NV':4,'AZ':4,'ND':4,'SD':4,'NE':4,'KS':4,'OK':4,'TX':4,'MT':4,'WY':4,'CO':4,'NM':4,
                   'UT':4,'ID':4,'OR':4,'WA':4,'AK':4,'HI':4}

    location_state = fields.Selection(string="Select you State",selection=[('DF','No State'),('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),
                                        ('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('FL','Florida'),
                                        ('GA','Georgia'),('HI','Hawái'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),
                                        ('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),
                                        ('MA','Massachusetts'),('MI','Míchigan'),('MN','Minnesota'),('MS','Mississippi'),
                                        ('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NV','Nevada'),('NH','New Hampshire'),
                                        ('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),
                                        ('OH','Ohio'),('OK','Oklahoma'),('OR','Oregón'),('PA','Pennsylvania'),('RI','Rhode Island'),
                                        ('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),
                                        ('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),
                                        ('WY','Wyoming')],copy=False,default='DF',ondelete='cascade')
   

    @api.depends('location_state','user_id','company_id')
    def _compute_warehouse_id(self):
        for sale in self:
            print(sale.location_state)
            if sale.state in ['draft','sent']or not sale.ids:
                sale.warehouse_id = sale.warehouse_dic[sale.location_state]
            else:
                super()._compute_warhouse_id()