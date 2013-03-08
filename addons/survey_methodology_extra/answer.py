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

class answer(osv.osv):
    """"""
    _name = 'survey_methodology.answer'
    _inherit = [ _name ]

    def _get_progress(self, cr, uid, ids, name, attrs, context=None):
        """"""
        r = {}
        for i in ids:
            r[i] = 0
        return r

    _columns = {
        'progress': fields.function(_get_progress, type='float', arg=None, fnct_inv_arg=None, obj=None, string='progress', readonly=True),
    }

    def is_valid(self, cr, uid, ids, context=None):
        """"""
        import pdb; pdb.set_trace()
        return {}

    def onchange_input(self, cr, uid, ids, input, context=None):
        """"""
        import pdb; pdb.set_trace()
        return {}

answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
