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

class node_copy(osv.TransientModel):
    """"""
    
    _name = 'sondaggio.node_copy'
    _inherit = [ _name ]


    def do_copy(self, cr, uid, ids, context=None):
        """"""
        obj_node = self.pool.get('sondaggio.node')
        context = context or {}
        if 'active_ids' not in context:
                return
        to_copy = context['active_ids']

        for wzd in self.browse(cr, uid, ids):
                new_parent_node_id = wzd.new_parent_node_id.id
                base_parent_place = wzd.new_parent_node_id.complete_place
                new_order = wzd.new_order
                max_level = wzd.max_level
                move = wzd.move
                if move:
                        obj_node.write(cr, uid, to_copy, { 'parent_id': new_parent_node_id })
                else:
                        for id in to_copy:
                                val = dict(
                                           parent_id=new_parent_node_id,
                                           complete_place=(base_parent_place, new_order+to_copy.index(id)),
                                           answers_ids=[],
                                          )
                                new_id = obj_node.copy(cr, uid, id, default=val, context=context)
        return {}

