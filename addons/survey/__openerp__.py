# -*- coding: utf-8 -*-
##############################################################################
#
#    Survey module.
#    Copyright (C) 2013 Moldeo Interactive
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
    'author': u'Moldeo Interactive',
    'category': 'base.module_category_hidden',
    'demo_xml': [],
    'depends': [],
    'description': u'Survey module.',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Survey module.',
    'test': [],
    'update_xml': [   u'security/survey_group.xml',
                      u'view/category_view.xml',
                      u'view/question_view.xml',
                      u'view/survey_view.xml',
                      u'view/answer_view.xml',
                      u'view/answer_text_view.xml',
                      u'view/answer_integer_view.xml',
                      u'view/answer_selection_view.xml',
                      u'view/options_view.xml',
                      u'view/survey_menuitem.xml',
                      u'workflow/survey_workflow.xml',
                      'security/ir.model.access.csv'],
    'version': u'1.0',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
