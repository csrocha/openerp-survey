# -*- coding: utf-8 -*-
##############################################################################
#
#    In statistics, survey methodology is the field that studies the sampling of individuals from a population with a view towards making statistical inferences about the population using the sample. This addon help to manage a survey in proffesional way.
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

class survey(osv.osv):
    """"""
    _name = 'survey_methodology.survey'
    _description = 'survey'

    _states_ = [
        # State machine: untitle
        ('draft','Draft'),
        ('accepted','Accepted'),
        ('published','Published'),
        ('close','Close'),
        ('cancelled','Cancelled'),
    ]

    _columns = {
        'name': fields.char(string='name', readonly=True, required=True, states={'draft':[('readonly',False)]}),
        'description': fields.text(string='description', readonly=True, states={'draft':[('readonly',False)]}),
        'creator_id': fields.many2one('res.partner', string='creator_id', readonly=True, states={'draft':[('readonly',False)]}),
        'open_dt': fields.datetime(string='open_dt', readonly=True, states={'draft':[('readonly',False)]}),
        'close_dt': fields.datetime(string='close_dt', readonly=True, states={'draft':[('readonly',False)]}),
        'automatic': fields.boolean(string='automatic', readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection(_states_, "State"),
        'question_ids': fields.many2many('survey_methodology.question', 'survey_methodology_survey_ids_question_ids_rel', 'question_ids', 'survey_ids', string='question_ids'), 
        'answer_ids': fields.one2many('survey_methodology.answer', 'survey_id', string='answer_ids'), 
        'partner_ids': fields.many2many('res.partner', 'survey_methodology_survey_ids_partner_ids_rel', 'partner_ids', 'survey_ids', string='partner_ids'), 
    }

    _defaults = {
        'state': 'draft',
    }

    def generate_questions(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'survey_methodology.survey', obj_id, cr)
            wf_service.trg_create(uid, 'survey_methodology.survey', obj_id, cr)
        return True


survey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
