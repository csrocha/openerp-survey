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

class enable_condition(osv.osv):
    """"""
    
    _name = 'sondaggio.enable_condition'
    _description = 'enable_condition'



    _columns = {
        'operator': fields.selection([(u'==', '=='), (u'!=', '!='), (u'>', '>'), (u'>=', '>='), (u'<', '<'), (u'<=', '<='), (u'in', 'in'), (u'not in', 'not in')], string='Operator'),
        'value': fields.char(string='Value'),
        'node_id': fields.many2one('sondaggio.node', string='node_id', ondelete='cascade', required=True), 
        'operated_node_id': fields.many2one('sondaggio.node', string='Variable', domain=[('type','=','Variable')], required=True), 
    }

    _defaults = {
        'node_id': lambda self, cr, uid, context=None: context and context.get('node_id', False),
    }


    _constraints = [
    ]




enable_condition()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
