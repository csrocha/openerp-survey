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

class caster(osv.osv):
    """"""
    _name = 'survey_methodology.caster'
    _description = 'caster'

    _states_ = [
    ]

    _columns = {
        'name': fields.char(string='Name'),
        'code': fields.text(string='Lambda Python Code'),
        'code_error': fields.text(string='Code error', readonly=True),
        'is_valid': fields.boolean(string='Is Valid?', readonly=True),
        'input_test_ids': fields.one2many('survey_methodology.input_test', 'caster_id', string='Input tests'), 
    }

    _defaults = {
    }

    def onchange_code(self, cr, uid, ids, code, input_test_ids, context=None):
        """"""
        raise NotImplementedError


caster()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
