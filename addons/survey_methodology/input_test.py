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

class input_test(osv.osv):
    """"""
    _name = 'survey_methodology.input_test'
    _description = 'input_test'

    _states_ = [
    ]

    _columns = {
        'name': fields.char(string='Name'),
        'input': fields.text(string='Input'),
        'as_integer': fields.integer(string='As integer'),
        'as_char': fields.char(string='As character'),
        'as_text': fields.text(string='As text'),
        'as_boolean': fields.boolean(string='As boolean'),
        'as_float': fields.float(string='As float'),
        'is_valid': fields.boolean(string='Is Valid'),
        'validator_id': fields.many2one('survey_methodology.validator', string='Validator'), 
        'caster_id': fields.many2one('survey_methodology.caster', string='Caster'), 
    }

    _defaults = {
    }


input_test()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
