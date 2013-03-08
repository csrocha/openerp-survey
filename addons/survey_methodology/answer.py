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
        'code': fields.char(string='Code', readonly=True, required=True),
        'name': fields.char(string='Question', readonly=True, required=True),
        'respondent_id': fields.many2one('res.partner', string='Respondent', readonly=True, required=True),
        'pollster_id': fields.many2one('res.users', string='Pollster', readonly=True),
        'progress': fields.function(_get_progress, type='float', arg=None, fnct_inv_arg=None, obj=None, string='Progress', readonly=True),
        'input': fields.char(string='Input', readonly=True, states={'enabled':[('readonly',False)]}),
        'input_as_integer': fields.integer(string='As integer number'),
        'input_as_char': fields.char(string='As text'),
        'input_as_boolean': fields.boolean(string='As boolean'),
        'input_as_float': fields.float(string='As real number'),
        'validator_id': fields.many2one('survey_methodology.validator', string='Validator', readonly=True),
        'caster_id': fields.many2one('survey_methodology.caster', string='Caster function', readonly=True),
        'message': fields.char(string='Message', readonly=True),
        'state': fields.selection(_states_, "State"),
        'question_id': fields.many2one('survey_methodology.question', string='Question', readonly=True, required=True), 
        'survey_id': fields.many2one('survey_methodology.survey', string='Survey', readonly=True, ondelete='cascade', required=True), 
        'respondent_code': fields.related(
                    'respondent_id',
                    'respondent_code',
                    type='char',
                    relation='res.partner',
                    string='Respondent Code', readonly=True, store=True
                    ),
    }

    _defaults = {
        'state': 'enabled',
    }

    _order = "survey_id, pollster_id, respondent_id, code"

    _constraints = [
    ]

    _sql_constraints = [ ('unique_answer','unique(survey_id,pollster_id,respondent_id,code)','Not repeat answers.') ]

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
            wf_service.trg_delete(uid, 'survey_methodology.answer', obj_id, cr)
            wf_service.trg_create(uid, 'survey_methodology.answer', obj_id, cr)
        return True



answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
