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

class answer(osv.osv):
    """"""
    _name = 'survey_methodology.answer'
    _description = 'answer'

    def _get_progress(self, cr, uid, ids, name, attrs, context=None):
        """"""
        raise NotImplementedError

    _states_ = [
        # State machine: untitle
        ('enabled','enabled'),
        ('disabled','disabled'),
        ('closed','closed'),
    ]

    _columns = {
        'name': fields.char(string='name', readonly=True, required=True),
        'responder_id': fields.many2one('res.partner', string='responder_id', readonly=True, required=True),
        'surveyor_id': fields.many2one('res.users', string='surveyor_id', readonly=True),
        'progress': fields.float(string='progress', readonly=True),
        'input': fields.char(string='Input', readonly=True, states={'enabled':[('readonly',False)]}),
        'input_as_integer': fields.integer(string='as integer number'),
        'input_as_char': fields.char(string='as text'),
        'input_as_boolean': fields.boolean(string='as boolean'),
        'input_as_float': fields.float(string='as real number'),
        'validator_id': fields.many2one('survey_methodology.validator', string='validator_id', readonly=True),
        'caster_id': fields.many2one('survey_methodology.caster', string='caster_id', readonly=True),
        'message': fields.char(string='message', readonly=True),
        'state': fields.selection(_states_, "State"),
        'question_id': fields.many2one('survey_methodology.question', string='Question', readonly=True, required=True), 
        'survey_id': fields.many2one('survey_methodology.survey', string='Survey', readonly=True, required=True), 
        'survey_code': fields.related(
                    'responder_id',
                    'survey_code',
                    type='integer',
                    relation='res.partner',
                    string='survey_code', readonly=True
                    ),
    }

    _defaults = {
        'state': 'enabled',
    }

    def is_valid(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_enabled(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'enabled'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'survey_methodology.answer', obj_id, cr)
            wf_service.trg_create(uid, 'survey_methodology.answer', obj_id, cr)
        return True


answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
