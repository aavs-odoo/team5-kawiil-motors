{
    "name": "Motorcycle Registry Manufacturing Enhancements",
    
    "summary": "Integrates Motorcycle Registry with the inventory app.",
    
    "description": """
    Motorcycle Registry Manufacturing Enhancements
====================
    This Module creates an entry in the motorcycle registry when the final delivery order is validated.
    """,
    
    "version": "0.1",
    
    "category": "Kauil/Registry",
    
    "license": "OPL-1",
    
    "depends": ["stock", "mrp", "motorcycle_registry", "sale","ge06_team05"],
    
    "data": [
        'views/motorcycle_registry_views.xml',
    ],
    
    "demo": [
        "demo/motorcycle_registry_demo.xml",
        "demo/product_demo.xml",
    ],
    
    "author": "kauil-motors",
    
    "website": "www.odoo.com",
    
    "application": True,
    
}