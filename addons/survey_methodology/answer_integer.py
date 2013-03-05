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

class answer_integer(osv.osv):
    """"""
    _name = 'survey_methodology.answer'
    _inherits = {  }
    _inherit = [ 'survey_methodology.answer' ]

    def _get_progress(self, cr, uid, ids, name, attrs, context=None):
        """"""
        member = getattr(self.pool.get('survey_methodology.answer'), '_get_progress')
        return member(cr, uid, ids, name, attrs)

    _states_ = [
    ]

    _columns = {
        'in_integer': fields.integer(string='in_integer'),
    }

    _defaults = {
    }

    def is_valid(self, cr, uid, ids, context=None):
        """"""
        member = getattr(self.pool.get('survey_methodology.answer'), 'is_valid')
        return member(cr, uid, ids)


answer_integer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
