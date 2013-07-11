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

class input_test(osv.osv):
    """"""
    
    _name = 'sondaggio.input_test'
    _description = 'input_test'



    _columns = {
        'name': fields.char(string='Name'),
        'formated': fields.text(string='Formated'),
        'valid': fields.boolean(string='Validation expected'),
        'question_id': fields.many2one('sondaggio.node', string='question_id'),
        'format_id': fields.many2one('sondaggio.format', string='format_id', ondelete='cascade'), 
    }

    _defaults = {
        'format_id': lambda self, cr, uid, context=None: context and context.get('format_id', False),
    }


    _constraints = [
    ]




input_test()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
