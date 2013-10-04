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

class questionnaire(osv.osv):
    """"""
    
    _name = 'sondaggio.questionnaire'
    _description = 'questionnaire'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: untitle
        ('draft','Draft'),
        ('waiting','Waiting'),
        ('in_process','In Process'),
        ('complete','Complete'),
        ('in_coding','In Coding'),
        ('validated','Validated'),
        ('rejected','Rejected'),
        ('cancelled','Cancelled'),
    ]
    _track = {
        'state': {
            'sondaggio.questionnaire_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'draft',
            'sondaggio.questionnaire_waiting': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'waiting',
            'sondaggio.questionnaire_in_process': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'in_process',
            'sondaggio.questionnaire_complete': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'complete',
            'sondaggio.questionnaire_in_coding': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'in_coding',
            'sondaggio.questionnaire_validated': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'validated',
            'sondaggio.questionnaire_rejected': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'rejected',
            'sondaggio.questionnaire_cancelled': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'cancelled',
        },
    }


    _columns = {
        'name': fields.char(string='Name', readonly=True, states={'draft':[('readonly',False)]}),
        'respondent_id': fields.many2one('res.partner', string='Respondent', readonly=True, states={'draft':[('readonly',False)]}),
        'pollster_id': fields.many2one('res.users', string='Pollster', readonly=True, states={'draft':[('readonly',False)]}),
        'code': fields.char(string='Code', readonly=True, states={'draft':[('readonly',False)]}),
        'channel': fields.selection([(u'online', 'online'), (u'personal', 'personal'), (u'telephonic', 'telephonic'), (u'offline', 'offline'), (u'mailing', 'mailing')], string='Channel', readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection(_states_, "State"),
        'survey_id': fields.many2one('sondaggio.survey', string='Survey', readonly=True, ondelete='cascade', required=True), 
        'respondent_code': fields.related(
                    'respondent_id',
                    'respondent_code',
                    type='char',
                    relation='res.partner',
                    string='Respondent Code', readonly=True, store=True
                    ),
        'parameter_ids': fields.one2many('sondaggio.parameter', 'questionnaire_id', string='Parameters'), 
        'communication_batch_ids': fields.many2many('sondaggio.communication_batch', 'sondaggio_communication_batch_ids_questionnaire_ids_rel', 'questionnaire_id', 'communication_batch_id', string='communication_batch_ids'), 
        'estrato_id': fields.many2one('sondaggio.estrato', string='estrato_id', readonly=True, required=True), 
        'sent_mail_id': fields.many2one('mail.mail', string='Sent Mails', required=True), 
        'answer_ids': fields.one2many('sondaggio.answer', 'questionnaire_id', string='answer_ids', select=True), 
    }

    _defaults = {
        'state': 'draft',
        'respondent_id': lambda self, cr, uid, context=None: context and context.get('respondent_id', False),
        'code': lambda self, cr, uid, context=None: context and context.get('code', False),
        'pollster_id': lambda self, cr, uid, context=None: context and context.get('pollster_id', False),
        'channel': lambda self, cr, uid, context=None: context and context.get('channel', False),
        'survey_id': lambda self, cr, uid, context=None: context and context.get('survey_id', False),
    }


    _constraints = [
    ]

    _sql_constraints = [  ]

    def start(self, cr, uid, ids, context=None):
        """Start is an action which leave you to start to complete the questionnaire.
Registry in the log start action."""
        raise NotImplementedError

    def on_open_ui(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def next_page(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def refresh_page(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def fields_view_get_callcenter(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def fields_view_get_dataentry(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def fields_view_get_online(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def onchange_input(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'sondaggio.questionnaire', obj_id, cr)
            wf_service.trg_create(uid, 'sondaggio.questionnaire', obj_id, cr)
        return True



questionnaire()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
