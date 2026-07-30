{
    'name': 'MC Davidian Newsletter Templates',
    'version': '17.0.1.13.0',
    'category': 'Marketing',
    'summary': 'Templates newsletter premium pour MC Davidian',
    'description': """
        Templates email marketing pour MC Davidian, accessoires cheveux de luxe.
        Design premium rose poudré, responsive, compatible mass mailing Odoo 17.
        Inclut versions FR (mcdavidian.fr) et EN (mcdavidian.com).
        + 6 templates de prospection B2B first-touch (MCD Prospection FR)
        + 6 templates de prospection B2B first-touch en anglais (MCD Prospection EN),
        disponibles en QWeb themes (picker) et mail.template (automation).
        EN templates utilisables pour Phase 2 (Northern Europe) et Phase 5 (World).
    """,
    'author': 'MC Davidian',
    'website': 'https://www.mcdavidian.com',
    'depends': ['mass_mailing'],
    'data': [
        'views/themes_templates.xml',
        'views/themes_prospection_fr.xml',
        'views/themes_prospection_en.xml',
        'views/snippets_themes.xml',
        'data/prospection_templates_fr.xml',
        'data/prospection_templates_en.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
