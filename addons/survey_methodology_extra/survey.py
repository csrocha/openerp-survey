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
import random
import itertools

class survey(osv.osv):
    """"""
    _name = 'survey_methodology.survey'
    _inherit = [ _name ]

    def generate_sample(self, cr, uid, ids, context=None):
        """"""
        context = context or {}
        partner_obj = self.pool.get('res.partner')

        for survey in self.browse(cr, uid, ids, context):
            sample_size = survey.sample_size
            sample_filter = survey.sample_filter and eval(survey.sample_filter) or []
            responder_ids = partner_obj.search(cr, uid, [('is_responder','=',True)] + sample_filter)
            sample_ids = random.sample(responder_ids, sample_size)
            self.write(cr, uid, survey.id, {'responder_ids': [(6,0,sample_ids)] })

        return True

    def generate_questions(self, cr, uid, ids, context=None):
        """"""
        context = context or {}
        partner_obj = self.pool.get('res.partner')
        user_obj = self.pool.get('res.partner')
        question_obj = self.pool.get('survey_methodology.question')
        answer_obj = self.pool.get('survey_methodology.answer')

        for survey in self.browse(cr, uid, ids, context):
            survey_id = survey.id
            root_question_id = survey.question_id.id
            question_ids  = [root_question_id] + survey.question_id.get_childs()[root_question_id]
            responder_ids = [ p.id for p in survey.responder_ids ] or partner_obj.search(cr, uid, [('is_responder','=',True)])
            surveyor_ids  = [ p.id for p in survey.surveyor_ids ] or user_obj.search(cr, uid, [])
            if len(surveyor_ids) == 0:
                osv.except_osv('No exists surveyor', 'Please create surveyors first')
            s_i = 0
            s_s = len(surveyor_ids)
            for question_id, responder_id in itertools.product(question_ids, responder_ids):
                v = {
                    'name': question_obj.browse(cr, uid, question_id).name,
                    'responder_id': responder_id,
                    'question_id': question_id,
                    'survey_id': survey_id,
                    'surveyor_id': surveyor_ids[s_i],
                }
                answer_obj.create(cr, uid, v)
                s_i = (s_i + 1) % s_s
            self.write(cr, uid, survey.id, {'state': 'accepted' })
        return True

survey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
