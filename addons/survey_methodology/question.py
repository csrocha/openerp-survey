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
    
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from survey_methodology_question where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _name = 'survey_methodology.question'
    _description = 'question'

    def _place_get_fnc(self, cr, uid, ids, name, args, context=None):
        """"""
        raise NotImplementedError

    _columns = {
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name', store=True),
        'name': fields.char(string='Code', required=True),
        'place': fields.integer(string='Place', required=True),
        'question': fields.char(string='Question', required=True),
        'type': fields.selection([(u'View', 'View'), (u'Variable', 'Variable'), (u'Null', 'Null')], string='Type', required=True),
        'variable_name': fields.char(string='Variable name'),
        'format_id': fields.many2one('survey_methodology.format', string='Format', select=True),
        'initial_state': fields.selection([(u'closed', 'closed'), (u'disabled', 'disabled'), (u'enabled', 'enabled')], string='Initial state', required=True),
        'next_enable': fields.text(string='Next enable rules'),
        'note': fields.text(string='Description'),
        'complete_place': fields.function(_place_get_fnc, type='char', arg=None, fnct_inv_arg=None, obj=None, string='complete_place', select=True, store=True),
        'page': fields.integer(string='page'),
        'survey_id': fields.many2one('survey_methodology.survey', string='Surveis', ondelete='cascade', required=True), 
        'answers_ids': fields.one2many('survey_methodology.answer', 'question_id', string='Answers'), 
        'parent_id': fields.many2one('survey_methodology.question', string='Parent'), 
        'child_ids': fields.one2many('survey_methodology.question', 'parent_id', string='Childs'), 
        'category_ids': fields.many2many('survey_methodology.category', 'survey_methodology_question_ids_category_ids_rel', 'category_ids', 'question_ids', string='Categories'), 
    }

    _defaults = {
        'next_enable': '',
        'type': 'View',
        'initial_state': 'disabled',
        'survey_id': lambda self, cr, uid, context=None: context and context.get('survey_id', False),
        'parent_id': lambda self, cr, uid, context=None: context and context.get('parent_id', False),
    }

    _order = "survey_id, complete_place, name"

    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive question.', ['parent_id'])
    ]

    _sql_constraints = [ ('unique_question', 'unique(survey_id, parent_id, place, name)','Not repeat questions in the same survey, parent, order and code'), ('unique_question', 'unique(complete_name)','Not repeat code in the same parent.') ]

    def next_place(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def onchange_parent_id(self, cr, uid, ids, parent_id, context=None):
        """"""
        raise NotImplementedError



question()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
