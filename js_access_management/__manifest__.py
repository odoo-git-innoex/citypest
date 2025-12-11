{
    "name": "Access Rights Management",
    "version": "17.0.1.0.0",
    "summary": """Access Rights Management""",
    "description": """Access Rights Management""",
    "author": "MuhammadJasim",
    "website": "https://github.com/jasimbassam0",
    "license": "OPL-1",
    "category": "Extra Tools",
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/access_management_view.xml",
        "views/res_users_view.xml",
    ],
    "depends": [
        "web",
    ],
    "post_init_hook": "post_install_action_dup_hook",
    "application": True,
    "auto_install": False,
}
