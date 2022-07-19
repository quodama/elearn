# -*- coding: utf-8 -*-
{
    'name': "elearn",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/res_partner_category_data.xml',
        #'views/views.xml',
        #'views/templates.xml',
        'views/period_views.xml',
        'views/schedule_views.xml',
        'views/curse_views.xml',
        'wizzard/elaran_matricu_wizzard_view.xml',
        'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}
