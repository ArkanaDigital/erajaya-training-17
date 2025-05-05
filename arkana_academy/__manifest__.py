# -*- coding: utf-8 -*-
{
    'name': "Arkana Academy",

    'summary': "This addons is generated for Arkana Academy",

    'description': """
The complete description of Arkana Academy
    """,

    'author': "PT Arkana Solusi Digital",
    'website': "https://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'data/course_data.xml',
        'data/scheduled_action_data.xml',
        'data/sequence_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/session_add_wizard_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/session_stage_views.xml',
        'views/partner_views.xml',
        'views/mail_session_attendee_confirmation_template.xml',
        'views/mail_session_upcoming_reminder_template.xml',
        'views/course_statistic_view_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}