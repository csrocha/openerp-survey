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

class format(osv.osv):
    """"""
    
    _name = 'survey_methodology.format'
    _description = 'format'

    _states_ = [
    ]

    _columns = {
        'name': fields.char(string='Name'),
        'validation': fields.text(string=''),
        'formating': fields.text(string=''),
        'tests_result': fields.boolean(string='Test result', readonly=True),
        'compile_message': fields.html(string='Compile message', readonly=True),
        'input_test_ids': fields.one2many('survey_methodology.input_test', 'format_id', string='Test inputs'), 
        'message_ids': fields.one2many('survey_methodology.message', 'format_id', string='Messages'), 
    }

    _defaults = {
    }


    _constraints = [
    ]


    def onchange_code(self, cr, uid, ids, validation, formating, message_ids, input_test_ids, context=None):
        """"""
        raise NotImplementedError

    def evaluate(self, cr, uid, ids, input, context=None):
        """"""
        raise NotImplementedError



format()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
