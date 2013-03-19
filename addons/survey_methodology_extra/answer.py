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

    """
    def write(self, cr, uid, ids, values, context=None):
        question_obj = self.pool.get('survey_methodology.question')
        wf_service = netsvc.LocalService("workflow")

        if 'input' in values:
            import pdb; pdb.set_trace()
            for ans in self.browse(cr, uid, ids):
                if ans.question_id.next_enable:
                    # Actualizamos los estados de las nuevas preguntas.
                    for lines in ans.question_id.next_enable.split('\n'):
                        condition, next_enable = lines.split(':')
                        next_ans = self.search(cr, uid, [
                            ('questionnaire_id','=',ans.questionnaire_id.id),
                            ('code', '=', next_enable)
                        ])
                        if next_ans and eval(condition, { 'self': next_ans[0] }):
                            self.write(cr, uid, next_ans, {'state': 'enabled'})
                            #print self.read(cr, uid, next_ans, ['state'])
                            #import pdb; pdb.set_trace()
                            #r = wf_service.trg_validate(uid, 'survey_methodology.ans', next_ans[0], 'sgn_enable', cr)
                            #print self.read(cr, uid, next_ans, ['state'])
                    # Aqui validariamos

        return super(answer, self).write(cr, uid, ids, values, context=context)
    """

    def set_status(self, cr, uid, names, state):
        """
        """
        question_obj = self.pool.get('survey_methodology.question')
        complete_names = [ to if ' / ' in to else to.replace('_', ' / ') for to in names ]
        q_ids = question_obj.search(cr, uid, [('complete_name','in',complete_names)])
        a_ids = self.search(cr, uid, [('question_id','in',q_ids)])
        self.write(cr, uid, a_ids, {'state': state})

    def onchange_input(self, cr, uid, ids, input, context=None):
        """"""
        me = self.browse(cr, uid, ids)[0]
        next_enable = me.question_id.next_enable
        condition, nexts = next_enable.split(':',1)
        if ':' in nexts:
            to_enable, to_disable = nexts.split(':')
            to_enable = to_enable.split(',')
            to_disable = to_disable.split(',')
        else:
            to_enable, to_disable = nexts.split(','), []

        self.set_status(cr, uid, to_enable, 'enabled')
        self.set_status(cr, uid, to_disable, 'disabled')

        return True

answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
