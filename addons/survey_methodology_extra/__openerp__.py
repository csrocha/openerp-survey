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
    'depends': ['survey_methodology','mail'],
    'description': u'In statistics, survey methodology is the field that studies the sampling of individuals from a population with a view towards making statistical inferences about the population using the sample. This addon help to manage a survey in proffesional way.',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Adaptation for Survey Methodology',
    'test': [
        'test/partners.yml',
        'test/questions.yml',
        'test/survey001.yml',
    ],
    'update_xml': [
        u'data/surveyors.xml',
        u'data/responders.xml',
        u'data/survey.xml',
        u'data/formats.xml',
        u'data/survey_methodology.input_test.csv',
        u'data/questions.xml',
#       u'security/survey_methodology_group.xml',
#       u'view/category_view.xml',
        u'view/questionnaire_view.xml',
        u'view/question_editor.xml',
        u'view/question_view.xml',
        u'view/partner_view.xml',
        u'view/survey_view.xml',
        u'view/answer_view.xml',
        u'view/format_view.xml',
#       u'view/answer_text_view.xml',
#       u'view/answer_integer_view.xml',
#       u'view/answer_selection_view.xml',
#       u'view/options_view.xml',
#       u'view/survey_methodology_menuitem.xml',
#       u'data/category_properties.xml',
#       u'data/question_properties.xml',
#       u'data/survey_properties.xml',
#       u'data/answer_properties.xml',
#       u'data/answer_text_properties.xml',
#       u'data/answer_integer_properties.xml',
#       u'data/answer_selection_properties.xml',
#       u'data/options_properties.xml',
#       u'workflow/survey_workflow.xml',
#       u'security/ir.model.access.csv'
    ],
    'css' : [
        'static/src/css/survey.css',
        'static/src/css/question.css',
    ],
    'version': u'1.0',
    'website': 'http://business.moldeo.coop/'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
