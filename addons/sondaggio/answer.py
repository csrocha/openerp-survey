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

class answer(osv.osv):
    """"""
    
    _name = 'sondaggio.answer'
    _description = 'answer'

    def _get_progress(self, cr, uid, ids, name, attrs, context=None):
        """"""
        raise NotImplementedError

    _states_ = [
        # State machine: untitle
        ('enabled','enabled'),
        ('disabled','disabled'),
        ('closed','closed'),
        ('cancelled','cancelled'),
    ]


    _columns = {
        'name': fields.char(string='Question', readonly=True, required=True),
        'complete_place': fields.char(string='complete_place', readonly=True, required=True, select=True),
        'code': fields.char(string='Code', readonly=True, required=True),
        'input': fields.char(string='Input', readonly=True, states={'enabled':[('readonly',False)]}),
        'formated': fields.char(string='As integer number'),
        'message': fields.char(string='Message', readonly=True),
        'valid': fields.boolean(string='is Valid?', readonly=True),
        'state': fields.selection([(u'closed', 'closed'), (u'disabled', 'disabled'), (u'enabled', 'enabled')], string='state', required=True),
        'state': fields.selection(_states_, "State"),
        'question_id': fields.many2one('sondaggio.node', string='Question', readonly=True, select=True, required=True), 
        'questionnaire_id': fields.many2one('sondaggio.questionnaire', string='questionnaire_id', select=True, ondelete='cascade', required=True), 
    }

    _defaults = {
        'state': 'enabled',
        'state': 'disabled',
    }

    _order = "questionnaire_id, complete_place"

    _constraints = [
    ]

    _sql_constraints = [ ('unique_answer','unique(questionnaire_id,complete_place)','Not repeat answers.') ]

    def is_valid(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def onchange_input(self, cr, uid, ids, input, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_enabled(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'enabled'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'sondaggio.answer', obj_id, cr)
            wf_service.trg_create(uid, 'sondaggio.answer', obj_id, cr)
        return True



answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
