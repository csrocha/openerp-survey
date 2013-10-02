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
from openerp import netsvc
from openerp.osv import osv, fields

class category(osv.osv):
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
            cr.execute('select distinct parent_id from survey_methodology_category where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _name = 'survey_methodology.category'
    _description = 'category'

    _columns = {
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name', store=True),
        'name': fields.char(string='Name', required=True),
        'question_ids': fields.many2many('survey_methodology.question', 'survey_methodology_question_ids_category_ids_rel', 'category_id', 'question_id', string='Questions'), 
        'child_ids': fields.one2many('survey_methodology.category', 'parent_id', string='child_ids'), 
        'parent_id': fields.many2one('survey_methodology.category', string='parent_id'), 
    }

    _defaults = {
    }


    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive category.', ['parent_id'])
    ]




category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
