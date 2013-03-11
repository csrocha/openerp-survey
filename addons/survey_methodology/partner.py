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
        'is_respondent': fields.boolean(string='is responder?'),
        'is_surveyor': fields.boolean(string='is surveyor?'),
        'respondent_code': fields.char(string='Respondent code'),
        'questionnaire_id': fields.many2many('survey_methodology.questionnaire', 'survey_methodology_respondent_code___rel', 'questionnaire_id', 'respondent_code', string='&lt;no label&gt;'), 
    }

    _defaults = {
    }


    _constraints = [
    ]


    def generate_questions(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError



partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
