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
    _description = 'node_copy'



    _columns = {
        'new_parent_node_id': fields.many2one('sondaggio.node', string='Question Parent'),
        'new_order': fields.integer(string='Order'),
        'move': fields.boolean(string='Move'),
        'do_rename': fields.boolean(string='Do rename?'),
        'new_name': fields.char(string='New code'),
        'new_question': fields.char(string='New question'),
    }

    _defaults = {
        'new_order': 1,
        'new_name': "{name}_C",
        'new_question': "{question} (Copy)",
    }


    _constraints = [
    ]


    def do_copy(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError



node_copy()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
