{
    "name": "Warehouse automatic implementation",
    
    "summary": "Set warehouse default selection",
    
    "description": """
    Warehouse Default Selection
====================
This Module is used to set a Warehouse in a Sale Order as a default
    """,
    
    "version": "0.1",
    
    "category": "Kauil/Registry",
    
    "license": "OPL-1",
    
    "depends": ['stock','motorcycle_registry','sale_management','sale_stock'],
    
    "data": [
        'views/sale_template_inherit.xml',
# hay que eliminar lso archivos que no usas
    ],
    
    "demo": [
        
    ],
    
    "author": "dihg-odoo",
    
    "website": "dihg@odoo.com",
    
    "application": True,
    
}