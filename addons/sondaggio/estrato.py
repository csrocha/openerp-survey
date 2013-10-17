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

class estrato(osv.osv):
    """"""
    
    _name = 'sondaggio.estrato'
    _description = 'estrato'



    _columns = {
        'name': fields.char(string='name'),
        'sector': fields.char(string='sector'),
        'dimension': fields.integer(string='Dim'),
        'region': fields.char(string='Reg'),
        'var_es_4': fields.char(string='var_es_4'),
        'var_es_5': fields.char(string='var_es_5'),
        'tam_muestra': fields.integer(string='tam_muestra'),
        'cant_muestra_reemplazo': fields.integer(string='cant_muestra_reemplazo'),
        'questionnaire_ids': fields.one2many('sondaggio.questionnaire', 'estrato_id', string='questionnaire_ids', readonly=True), 
        'survey_id': fields.many2one('sondaggio.survey', string='survey_id', required=True), 
    }

    _defaults = {
        'survey_id': lambda self, cr, uid, context=None: context and context.get('survey_id', False),
    }


    _constraints = [
    ]




estrato()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
