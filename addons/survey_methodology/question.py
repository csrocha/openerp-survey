# -*- coding: utf-8 -*-
##############################################################################
#
#    In statistics, survey methodology is the field that studies the sampling of individuals from a population with a view towards making statistical inferences about the population using the sample. This addon help to manage a survey in proffesional way.
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


import re
import netsvc
from osv import osv, fields

class question(osv.osv):
    """"""
    _name = 'survey_methodology.question'
    _description = 'question'

    _states_ = [
    ]

    _columns = {
        'code': fields.char(string='Code', required=True),
        'name': fields.char(string='Name', required=True),
        'description': fields.text(string='Description'),
        'data_type': fields.selection([(u'Group', 'Group'), (u'Integer', 'Integer'), (u'Text', 'Text'), (u'Char', 'Char'), (u'Float', 'Float'), (u'Selection', 'Selection')], string='Data type', required=True),
        'size': fields.integer(string='Size'),
        'min': fields.integer(string='Min value'),
        'max': fields.integer(string='Max value'),
        'validation': fields.text(string='validation'),
        'survey_ids': fields.many2many('survey_methodology.survey', 'survey_methodology_survey_ids_question_ids_rel', 'survey_ids', 'question_ids', string='survey_ids'), 
        'answers_ids': fields.one2many('survey_methodology.answer', 'question_id', string='answers_ids'), 
        'parent_id': fields.many2one('survey_methodology.question', string='parent_id'), 
        'child_ids': fields.one2many('survey_methodology.question', 'parent_id', string='child_ids'), 
        'category_ids': fields.many2many('survey_methodology.category', 'survey_methodology_question_ids_category_ids_rel', 'category_ids', 'question_ids', string='category_ids'), 
        'selection_options_ids': fields.one2many('survey_methodology.options', 'question_selection_id', string='selection_options_ids'), 
    }

    _defaults = {
        'data_type': 'integer',
        'parent_id': lambda self, cr, uid, context=None: context and context.get('parent_id', False),
    }

    def onchange_type(self, cr, uid, ids, type, context=None):
        """"""
        raise NotImplementedError


question()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
