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

class communication_batch(osv.osv):
    """"""
    
    _name = 'sondaggio.communication_batch'
    _description = 'communication_batch'

    _states_ = [
        # State machine: untitle
        ('draft','Draft'),
        ('accepted','Accepted'),
        ('running','Running'),
        ('cancelled','Cancelled'),
        ('done','Done'),
    ]


    _columns = {
        'name': fields.char(string='Description', required=True),
        'email_parameter_name': fields.char(string='Parameter name', required=True),
        'email_subject': fields.char(string='Subject', required=True),
        'email_body': fields.html(string='Body', required=True),
        'email_reply_to': fields.char(string='Replay to', required=True),
        'email_copy_to': fields.char(string='Copy to'),
        'login_user_id': fields.many2one('res.users', string='Login User', required=True),
        'state': fields.selection(_states_, "State"),
        'survey_id': fields.many2one('sondaggio.survey', string='Survey', required=True), 
        'waiting_ids': fields.many2many('sondaggio.questionnaire', 'sondaggio_waiting_batch_ids_waiting_ids_rel', 'communication_batch_id', 'questionnaire_id', string='Questionnaire waiting to communication'), 
        'sent_mail_ids': fields.many2many('mail.mail', 'sondaggio_sent_mail_ids___rel', 'communication_batch_id', 'mail_id', string=''), 
    }

    _defaults = {
        'state': 'draft',
    }


    _constraints = [
    ]


    def do_publish(self, cr, uid, ids, context=None):
        """Completa la lista de waiting_questionnaire_ids a partir de los questionnaire_ids que hay en survey_id. Cambia a estado running."""
        raise NotImplementedError

    def send_mails(self, cr, uid, ids, context=None):
        """Envia un mail por cada waiting_questionnaires_ids usando los datos de la comunicación (email, subject, body, reply_to, etc) una vez enviado se borra de waiting y pasa a done_questionnaire_ids. Si no hay más emails en waiting se cambia a estado "done"."""
        raise NotImplementedError

    def action_wfk_set_cancelled(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'cancelled'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'sondaggio.communication_batch', obj_id, cr)
            wf_service.trg_create(uid, 'sondaggio.communication_batch', obj_id, cr)
        return True

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'sondaggio.communication_batch', obj_id, cr)
            wf_service.trg_create(uid, 'sondaggio.communication_batch', obj_id, cr)
        return True



communication_batch()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
