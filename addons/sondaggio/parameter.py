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

class parameter(osv.osv):
    """"""
    
    _name = 'sondaggio.parameter'
    _description = 'parameter'



    _columns = {
        'name': fields.char(string='name'),
        'value': fields.char(string='value'),
        'questionnaire_id': fields.many2one('sondaggio.questionnaire', string='questionnaire_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'questionnaire_id': lambda self, cr, uid, context=None: context and context.get('questionnaire_id', False),
    }


    _constraints = [
    ]




parameter()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
