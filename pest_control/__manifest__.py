{
    'name': "Pest Control Management",
    'version': '1.0',
    'category': 'Services',
    'summary': 'Custom module for pest control lead management',
    'depends': ['base', 'crm', 'website', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/pest_control_security.xml',
        'data/pest_control_data.xml',
        'data/sequence_data.xml',
        'views/pest_control_lead_views.xml',
        'views/web_templates.xml',
        'views/pest_control_actions.xml',
        'views/pest_control_menu.xml',
    ],
    'installable': True,
    'application': True,
}
