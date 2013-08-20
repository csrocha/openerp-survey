# -*- coding: utf-8 -*-
##############################################################################
#
#    Survey Methodology
#    Copyright (C) 2013 Coop. Trab. Moldeo Interactive Ltda.
#    info@moldeo.coop
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
    'auto_install': True,
    'author': u'Coop. Trab. Moldeo Interactive Ltda.',
    'category': 'base.module_category_hidden',
    'demo_xml': [],
    'depends': ['sondaggio','mail'],
    'description': u'In statistics, survey methodology is the field that studies the sampling of individuals from a population with a view towards making statistical inferences about the population using the sample. This addon help to manage a survey in proffesional way.',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Adaptation for Survey Methodology',
    'test': [
        'test/questionnaire_import.yml',
#        'test/partners.yml',
#       'test/questions.yml',
#       'test/survey001.yml',
#        u'data/surveyors.xml',
#        u'data/responders.xml',
#        u'data/survey.xml',
#        u'data/sondaggio.input_test.csv',
#        u'data/sondaggio.node.csv',
#       u'data/questions.xml',
#       u'security/sondaggio_group.xml',
#       u'view/category_view.xml',
    ],
    'update_xml': [
        u'data/formats.xml',
        u'view/questionnaire_view.xml',
        u'view/questionnaire_stats_view.xml',
        u'view/question_editor.xml',
        u'view/question_view.xml',
        u'view/partner_view.xml',
        u'view/survey_view.xml',
        u'view/answer_view.xml',
        u'view/format_view.xml',
        u'view/enable_condition_view.xml',
        u'view/communication_batch_view.xml',
        u'wizard/questionnaire_import_view.xml',
        u'data/online.xml',
        u'wizard/node_copy_view.xml',
    ],
    'css' : [
        'static/src/css/*.css',
    ],
    'js': [
        'static/src/js/*.js',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'version': u'1.0',
    'website': 'http://business.moldeo.coop/'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
