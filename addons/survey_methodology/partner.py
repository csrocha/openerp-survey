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

class partner(osv.osv):
    """"""
    _name = 'res.partner'
    _inherits = {  }
    _inherit = [ 'res.partner' ]

    _states_ = [
    ]

    _columns = {
        'is_responder': fields.boolean(string='is responder?'),
        'is_surveyor': fields.boolean(string='is surveyor?'),
        'survey_code': fields.integer(string='survey_code'),
        'answer_id': fields.many2many('survey_methodology.answer', 'survey_methodology___survey_code_rel', 'answer_id', 'survey_code', string='&lt;no label&gt;'), 
    }

    _defaults = {
    }


partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
