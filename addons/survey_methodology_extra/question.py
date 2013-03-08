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
import itertools

class question(osv.osv):
    """"""
    _name = 'survey_methodology.question'
    _inherit = [ _name ]

    def get_childs(self, cr, uid, ids, context=None):
        context = context or {}

        r = {}
        for question in self.browse(cr, uid, ids):
            qid = question.id
            r[qid] = [ q.id for q in question.child_ids ]
            if len(r[qid]) > 0:
                r[qid] += itertools.chain(*self.get_childs(cr, uid, r[qid], context).values())

        return r
    
question()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
