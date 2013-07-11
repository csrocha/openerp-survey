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

class node(osv.osv):
    """"""
    _name = 'sondaggio.node'
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
                cr.execute("SELECT max(place) FROM sondaggio_node WHERE parent_id = %s", (read['parent_id'][0],))
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
            cr.execute("update sondaggio_node set place=%s where id=%s", (value, ids))
            ids, complete_place = self.place_get(cr, uid, ids)[0]
            cr.execute("update sondaggio_node set complete_place=%s where id=%s", (complete_place, ids))
        del value

    _columns = {
        'place': fields.function(_get_place, fnct_inv=_set_place, type="integer", string='Place', store=True),
        'complete_place': fields.function(_place_get_fnc, type="char", string='Place Path', store=True),
    }

    def open_node(self, cr, uid, ids, context=None):
        model_obj = self.pool.get('ir.model.data')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Question',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sondaggio.node',
            #'view_id': model_obj.get_object_reference(cr, uid, 'sondaggio', 'view_sondaggio_node_form')[1],
            'res_id': ids[0],
            'context': context,
        }

    def reordering(self, cr, uid, ids, context=None):
        context = context or {}

        if type(ids) is int:
            ids = [ids]

        i = 1
        for q in self.read(cr, uid, ids, ['child_ids'], context=context):
            self.write(cr, uid, q['id'], { 'place': i })
            self.reordering(cr, uid, q['child_ids'], context=context)
            i = i + 1

    def answer_is_valid(self, cr, uid, ids, values, context=None):
        pass

    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()

        # No copy answers and childs
        default.update(
            answers_ids=False,
            child_ids=False
        )

        # Copy using default code
        rid = super(node, self).copy(cr, uid, id, default, context=context)

        # Copy childs
        #import pdb; pdb.set_trace()
        my_node = self.browse(cr, uid, id, context=context)
        copy_node = self.browse(cr, uid, rid, context=context)
        for child in my_node.child_ids:
            child_default = {
                'parent_id': copy_node.id,
                'survey_id': copy_node.survey_id.id,
            }
            child_ids = self.copy(cr, uid, child.id, child_default, context=context, done_list=done_list, local=True)

        return rid

node()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
