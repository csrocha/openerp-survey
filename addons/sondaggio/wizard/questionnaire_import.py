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

class questionnaire_import(osv.TransientModel):
    """"""
    
    _name = 'sondaggio.questionnaire_import'
    _description = 'questionnaire_import'

    _states_ = [
        # State machine: untitle
        ('init','Select Import File'),
        ('config','Select Name Field'),
        ('done','Ready'),
    ]


    _columns = {
        'in_file': fields.binary(string='Import file', states={'selectfile': [('invisible', False)]}),
        'survey_id': fields.many2one('sondaggio.survey', string='Survey', states={'selectfile': [('invisible', True)]}),
        'selected_column_id': fields.many2one('sondaggio.import_file_column', string='Column'),
        'state': fields.selection(_states_, "State"),
        'import_file_column_ids': fields.one2many('sondaggio.import_file_column', 'questionnaire_import_id', string='import_file_column_ids'), 
    }

    _defaults = {
        'state': 'init',
    }


    _constraints = [
    ]


    def do_load_file(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def do_import(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def do_continue(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError



questionnaire_import()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
