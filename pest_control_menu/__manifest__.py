{
    'name': 'Pest Control Menu',
    'version': '1.0',
    'summary': 'Custom module with a pest control menu and model',
    'category': 'Custom',
    'author': 'Your Name',
    'depends': ['base', 'fieldservice', 'site_survey', 'calendar', 'contacts', 'sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}

