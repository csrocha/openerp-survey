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
        'type': fields.selection([(u'Group', 'Group'), (u'Integer', 'Integer'), (u'Text', 'Text'), (u'Char', 'Char'), (u'Float', 'Float'), (u'Boolean', 'Boolean')], string='Type', required=True),
        'validator_id': fields.many2one('survey_methodology.validator', string='Validator'),
        'caster_id': fields.many2one('survey_methodology.caster', string='Caster'),
        'variable_name': fields.char(string='variable_name'),
        'initial_state': fields.selection([(u'closed', 'closed'), (u'disabled', 'disabled'), (u'enabled', 'enabled')], string='Initial state', required=True),
        'next_enable': fields.text(string='Next enable rules'),
        'survey_ids': fields.one2many('survey_methodology.survey', 'question_id', string='Surveis'), 
        'answers_ids': fields.one2many('survey_methodology.answer', 'question_id', string='Answers'), 
        'parent_id': fields.many2one('survey_methodology.question', string='Parent'), 
        'child_ids': fields.one2many('survey_methodology.question', 'parent_id', string='Childs'), 
        'category_ids': fields.many2many('survey_methodology.category', 'survey_methodology_question_ids_category_ids_rel', 'category_ids', 'question_ids', string='Categories'), 
    }

    _defaults = {
        'next_enable': '',
        'type': 'Group',
        'initial_state': 'closed',
        'parent_id': lambda self, cr, uid, context=None: context and context.get('parent_id', False),
    }


question()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
