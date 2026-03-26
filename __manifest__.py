{
    'name': 'MC Davidian Newsletter Templates',
    'version': '17.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Templates newsletter premium pour MC Davidian',
    'description': """
        Templates email marketing pour MC Davidian — accessoires cheveux de luxe.
        Design premium rose poudré, responsive, compatible mass mailing Odoo 17.
        Inclut versions FR (mcdavidian.fr) et EN (mcdavidian.com).
    """,
    'author': 'MC Davidian',
    'website': 'https://www.mcdavidian.com',
    'depends': ['mass_mailing'],
    'data': [
        'views/themes_templates.xml',
        'views/snippets_themes.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
