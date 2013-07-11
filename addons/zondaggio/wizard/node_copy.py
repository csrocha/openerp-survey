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
                target_survey_id = wzd.new_parent_node_id.survey_id.id
                base_parent_place = wzd.new_parent_node_id.complete_place
                new_order = wzd.new_order
                move = wzd.move
                do_rename = wzd.do_rename
                new_name = wzd.new_name
                new_question = wzd.new_question
                if move:
                        obj_node.write(cr, uid, to_copy, {
                                'parent_id': new_parent_node_id,
                                'survey_id': target_survey_id,
                        })
                else:
                        for id in to_copy:
                                node_data = obj_node.read(cr, uid, id, ['name', 'question'])
                                val = dict(
                                           parent_id=new_parent_node_id,
                                           survey_id=target_survey_id,
                                           complete_place="{0}{1:02X}".format(base_parent_place, new_order+to_copy.index(id)),
                                           question = (new_question if do_rename else "{question}").format(**node_data),
                                           name = (new_name if do_rename else "{name}").format(**node_data)
                                          )
                                new_id = obj_node.copy(cr, uid, id, default=val, context=context)
        return {}

