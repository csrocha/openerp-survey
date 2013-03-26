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

class category(osv.osv):
    """"""
    
    _name = 'survey_methodology.category'
    _description = 'category'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'question_ids': fields.many2many('survey_methodology.question', 'survey_methodology_question_ids_category_ids_rel', 'question_ids', 'category_ids', string='Questions'), 
        'child_ids': fields.one2many('survey_methodology.category', 'parent_id', string='child_ids'), 
        'parent_id': fields.many2one('survey_methodology.category', string='parent_id'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
