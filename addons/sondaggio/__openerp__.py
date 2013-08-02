# -*- coding: utf-8 -*-
##############################################################################
#
#    Survey Methodology
#    Copyright (C) 2013 Coop. Trab. Moldeo Interactive Ltda.
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{   'active': False,
    'author': u'Coop. Trab. Moldeo Interactive Ltda.',
    'category': 'base.module_category_hidden',
    'demo_xml': [],
    'depends': [u'mail'],
    'description': u'In statistics, survey methodology is the field that studies the sampling of individuals from a population with a view towards making statistical inferences about the population using the sample. This addon help to manage a survey in proffesional way.',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Survey Methodology',
    'test': [],
    'update_xml': [   u'security/sondaggio_group.xml',
                      u'view/node_view.xml',
                      u'view/category_view.xml',
                      u'view/format_view.xml',
                      u'view/input_test_view.xml',
                      u'view/control_condition_view.xml',
                      u'view/survey_view.xml',
                      u'view/communication_batch_view.xml',
                      u'view/enable_condition_view.xml',
                      u'view/answer_view.xml',
                      u'view/partner_view.xml',
                      u'view/message_view.xml',
                      u'view/parameter_view.xml',
                      u'view/questionnaire_view.xml',
                      u'data/node_properties.xml',
                      u'data/category_properties.xml',
                      u'data/format_properties.xml',
                      u'data/input_test_properties.xml',
                      u'data/control_condition_properties.xml',
                      u'data/survey_properties.xml',
                      u'data/communication_batch_properties.xml',
                      u'data/enable_condition_properties.xml',
                      u'data/answer_properties.xml',
                      u'data/partner_properties.xml',
                      u'data/message_properties.xml',
                      u'data/parameter_properties.xml',
                      u'data/questionnaire_properties.xml',
                      u'data/node_track.xml',
                      u'data/category_track.xml',
                      u'data/format_track.xml',
                      u'data/input_test_track.xml',
                      u'data/control_condition_track.xml',
                      u'data/survey_track.xml',
                      u'data/communication_batch_track.xml',
                      u'data/enable_condition_track.xml',
                      u'data/answer_track.xml',
                      u'data/partner_track.xml',
                      u'data/message_track.xml',
                      u'data/parameter_track.xml',
                      u'data/questionnaire_track.xml',
                      u'workflow/survey_workflow.xml',
                      u'workflow/answer_workflow.xml',
                      u'workflow/questionnaire_workflow.xml',
                      u'workflow/communication_batch_workflow.xml',
                      'security/ir.model.access.csv',
                      u'wizard/node_copy_view.xml',
                      u'wizard/questionnaire_import_view.xml',
                      u'wizard/import_file_column_view.xml',
                      u'wizard/questionnaire_import_workflow.xml',
                      u'view/sondaggio_menuitem.xml'],
    'version': u'1.0',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
