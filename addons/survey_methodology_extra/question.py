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
import itertools

class question(osv.osv):
    """"""
    _name = 'survey_methodology.question'
    _inherit = [ _name ]

    def place_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['place','parent_id'], context=context)
        res = []
        for record in reads:
            name = "%02X" % (record['place'] % 256)
            if record['parent_id']:
                preads = self.read(cr, uid, record['parent_id'][0], ['complete_place'], context=context)
                name = "%s%s" % (preads['complete_place'], name)
            res.append((record['id'], name[:32]))
        return res

    def _place_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.place_get(cr, uid, ids, context=context)
        return dict(res)

    def _get_place(self, cr, uid, ids, field, args, context=None):
        reads = self.read(cr, uid, ids, ['parent_id', 'place'])
        r = {}
        for read in reads:
            if read['parent_id'] and type(read['place']) is bool:
                cr.execute("SELECT max(place) FROM survey_methodology_question WHERE parent_id = %s", (read['parent_id'][0],))
                order = cr.fetchall()
                if order and order[0] and order[0][0]:
                    r[read['id']] = order[0][0] + 1
                else:
                    r[read['id']] = 1
            elif type(read['place']) is int:
                r[read['id']] = read['place']
            else:
                r[read['id']] = 1
        return r

    def _set_place(self, cr, uid, ids, field, value, args, context=None):
        if value:
            cr.execute("update survey_methodology_question set place=%s where id=%s", (value, ids))
            ids, complete_place = self.place_get(cr, uid, ids)[0]
            cr.execute("update survey_methodology_question set complete_place=%s where id=%s", (complete_place, ids))
        del value

    _columns = {
        'place': fields.function(_get_place, fnct_inv=_set_place, type="integer", string='Place', store=True),
        'complete_place': fields.function(_place_get_fnc, type="char", string='Place Path', store=True),
    }

    def open_question(self, cr, uid, ids, context=None):
        model_obj = self.pool.get('ir.model.data')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Question',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'survey_methodology.question',
            'view_id': model_obj.get_object_reference(cr, uid, 'survey_methodology', 'view_survey_methodology_question_form')[1],
            'res_id': ids[0],
            'context': context,
        }

question()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
