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

class jump_condition(osv.osv):
    """"""
    
    _name = 'survey_methodology.jump_condition'
    _description = 'jump_condition'

    _columns = {
        'condition': fields.char(string='condition'),
        'question_id': fields.many2one('survey_methodology.question', string='&lt;no label&gt;', ondelete='cascade'), 
        'enable_question_ids': fields.many2many('survey_methodology.question', 'survey_methodology_enable_condition_ids_enable_question_ids_rel', 'jump_condition_id', 'question_id', string='enable_question_ids'), 
        'disable_question_ids': fields.many2many('survey_methodology.question', 'survey_methodology_disable_condition_ids_disable_question_ids_rel', 'jump_condition_id', 'question_id', string='disable_question_ids'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




jump_condition()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
