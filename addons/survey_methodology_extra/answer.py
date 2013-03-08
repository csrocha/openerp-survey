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
    _inherit = [ _name ]

    _sql_constraints = [('respondent_question_survey_uniq','unique(respondent_id, question_id, survey_id)', 'Answer must be unique!')]

    def _get_progress(self, cr, uid, ids, name, attrs, context=None):
        """"""
        r = {}
        for i in ids:
            r[i] = 0
        return r

    _columns = {
        'progress': fields.function(_get_progress, type='float', arg=None, fnct_inv_arg=None, obj=None, string='progress', readonly=True),
    }

    def is_valid(self, cr, uid, ids, context=None):
        """"""
        import pdb; pdb.set_trace()
        return {}

    def onchange_input(self, cr, uid, ids, input, context=None):
        """"""
        question_obj = self.pool.get('survey_methodology.question')

        answer = self.browse(cr, uid, ids)

        for question_id in answer.question_id.next().walk_to():
            v = {
                'name': question.name,
                'respondent_id': respondent_id,
                'question_id': question_id,
                'survey_id': survey_id,
                'pollster_id': context.get('pollster_id', False),
            }
            new_answer_id = self.create(cr, uid, v)



        import pdb; pdb.set_trace()
        return {}

answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
