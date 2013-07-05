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

class control_condition(osv.osv):
    """"""
    
    _name = 'sondaggio.control_condition'
    _description = 'control_condition'



    _columns = {
        'name': fields.char(string='Condition'),
        'survey_id': fields.many2one('sondaggio.survey', string='survey_id', ondelete='cascade', required=True), 
        'enable_node_ids': fields.many2many('sondaggio.node', 'sondaggio_enable_global_condition_ids_enable_node_ids_rel', 'control_condition_id', 'node_id', string='Enable'), 
        'disable_node_ids': fields.many2many('sondaggio.node', 'sondaggio_disable_global_condition_ids_disable_node_ids_rel', 'control_condition_id', 'node_id', string='Disable'), 
    }

    _defaults = {
        'survey_id': lambda self, cr, uid, context=None: context and context.get('survey_id', False),
    }


    _constraints = [
    ]




control_condition()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
