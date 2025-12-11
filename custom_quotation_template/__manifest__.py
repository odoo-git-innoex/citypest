# -*- coding: utf-8 -*-
{
    'name': 'Custom Quotation Template',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom quotation template with professional layout',
    'description': """
        Custom Quotation Template
        =========================
        
        This module extends the sales module to provide a custom quotation template
        with professional layout and formatting.
        
        Features:
        - Custom quotation template design
        - Professional header with company details
        - Enhanced layout for better presentation
        - Arabic and English support
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['sale_management', 'base'],
    'data': [
        'reports/custom_quotation_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
