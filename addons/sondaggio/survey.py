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

class survey(osv.osv):
    """Click to add a survey in your survey file."""
    
    _name = 'sondaggio.survey'
    _description = 'Click to add a survey in your survey file.'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: untitle
        ('draft','Draft'),
        ('accepted','Accepted'),
        ('published','Published'),
        ('close','Close'),
        ('cancelled','Cancelled'),
    ]
    _track = {
        'state': {
            'sondaggio.survey_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'draft',
            'sondaggio.survey_accepted': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'accepted',
            'sondaggio.survey_published': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'published',
            'sondaggio.survey_close': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'close',
            'sondaggio.survey_cancelled': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'cancelled',
        },
    }
    _columns = {
        'name': fields.char(string='Name', readonly=True, required=True, states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description', readonly=True, states={'draft':[('readonly',False)]}),
        'manager_id': fields.many2one('res.users', string='Survey Manager', readonly=True, states={'draft':[('readonly',False)]}),
        'open_dt': fields.datetime(string='Open date', readonly=True, states={'draft':[('readonly',False)]}),
        'close_dt': fields.datetime(string='Close date', readonly=True, states={'draft':[('readonly',False)]}),
        'automatic': fields.boolean(string='Automatic start', readonly=True, states={'draft':[('readonly',False)]}),
        'message': fields.text(string='Message to Responder', readonly=True, states={'draft':[('readonly',False)]}),
        'sample_size': fields.integer(string='Sample size', readonly=True, states={'draft':[('readonly',False)]}),
        'sample_filter': fields.char(string='Filter for the Sample', help=u"""Context filter for partner. This help to select partners to create the sample. For example: [(&quot;is_company&quot;,&quot;=&quot;,True)] Only select companies.""", readonly=True, size=512, states={'draft':[('readonly',False)]}),
        'state': fields.selection(_states_, "State"),
        'question_ids': fields.one2many('sondaggio.node', 'survey_id', string='Questions', readonly=True, states={'draft':[('readonly',False)]}), 
        'questionnaire_ids': fields.one2many('sondaggio.questionnaire', 'survey_id', string='Answers', readonly=True), 
        'respondent_ids': fields.many2many('res.partner', 'sondaggio_respond_ids_respondent_ids_rel', 'survey_id', 'partner_id', string='Responders', readonly=True, states={'draft':[('readonly',False)], 'published':[('readonly',False)],}), 
        'control_condition_ids': fields.one2many('sondaggio.control_condition', 'survey_id', string='control_condition_ids'), 
        'pollster_ids': fields.many2many('res.users', 'sondaggio_work_ids_pollster_ids_rel', 'survey_id', 'users_id', string='Surveyors', readonly=True, states={'draft':[('readonly',False)]}), 
    }

    _defaults = {
        'state': 'draft',
        'sample_filter': [],
        'manager_id': lambda self, cr, uid, *args, **argv: uid,
    }


    _constraints = [
    ]


    def generate_questions(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def generate_sample(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'sondaggio.survey', obj_id, cr)
            wf_service.trg_create(uid, 'sondaggio.survey', obj_id, cr)
        return True



survey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
