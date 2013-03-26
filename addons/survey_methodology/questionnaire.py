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

class questionnaire(osv.osv):
    """"""
    
    _name = 'survey_methodology.questionnaire'
    _description = 'questionnaire'

    _columns = {
        'name': fields.char(string='Name', readonly=True),
        'respondent_id': fields.many2one('res.partner', string='Respondent', readonly=True),
        'pollster_id': fields.many2one('res.users', string='Pollster', readonly=True),
        'survey_id': fields.many2one('survey_methodology.survey', string='Survey', readonly=True, ondelete='cascade', required=True), 
        'respondent_code': fields.related(
                    'respondent_id',
                    'respondent_code',
                    type='char',
                    relation='res.partner',
                    string='Respondent Code', readonly=True, store=True
                    ),
        'answer_ids': fields.one2many('survey_methodology.answer', 'questionnaire_id', string='answer_ids', select=True), 
    }

    _defaults = {
        'respondent_id': lambda self, cr, uid, context=None: context and context.get('respondent_id', False),
        'pollster_id': lambda self, cr, uid, context=None: context and context.get('pollster_id', False),
    }


    _constraints = [
    ]

    _sql_constraints = [  ]



questionnaire()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
