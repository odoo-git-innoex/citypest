{
    "name": "Site Survey",
    "version": "17.0.1.0.0",
    "category": "Services",
    "summary": "Manage site surveys per FSM Location",
    "depends": ["fieldservice_crm"],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/crm_stage.xml',
        'views/site_survey_views.xml',
        'views/crm_lead.xml',
        'views/survey_pest.xml',
    ],
    "installable": True,
    "application": True,
}

