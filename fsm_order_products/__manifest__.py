{
    'name': 'FSM Order Product Extension',
    'version': '1.1',
    'summary': 'Add products to FSM orders and auto-update inventory',
    'description': 'Extends Field Service Orders with product lines, quantity tracking, and auto-stock adjustment when executed or marked as completed.',
    'category': 'Field Service',
    'author': 'Your Name',
    'website': 'https://yourcompany.com',
    'depends': ['fieldservice', 'stock', 'fieldservice_crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/fsm_order_form.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

