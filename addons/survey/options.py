# -*- coding: utf-8 -*-
##############################################################################
#
#    Survey module.
#    Copyright (C) 2013 Moldeo Interactive
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


import netsvc
import re
from osv import osv, fields

class options(osv.osv):
    """"""
    _name = 'survey.options'
    _description = 'options'

    _states_ = [
    ]

    _columns = {
        'name': fields.char(string='name', required=True), 
        'question_selection_id': fields.many2one('survey.question', string='question_selection_id', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


options()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
