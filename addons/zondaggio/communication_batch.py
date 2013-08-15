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
import logging

class communication_batch(osv.osv):
    """"""
    
    _name = 'sondaggio.communication_batch'
    _inherit = 'sondaggio.communication_batch'

    def do_publish(self, cr, uid, ids=None,context=None):
        """Completa la lista de waiting_questionnaire_ids a partir de los questionnaire_ids que hay en survey_id. Cambia a estado running."""
        raise NotImplementedError


    def send_mails(self, cr, uid, ids, context=None):
        """Envia un mail por cada waiting_questionnaires_ids usando los datos de la comunicación (email, subject, body, reply_to, etc) una vez enviado se borra de waiting y pasa a done_questionnaire_ids. Si no hay más emails en waiting se cambia a estado "done"."""

        _logger = logging.getLogger(__name__)
        _logger.info('Sending communications by email...')
        mail_mail = self.pool.get('mail.mail')

        # Agregar al final de la URL
        questionnaire_url = "#action=questionnaire.ui&active_id=%(questionnaire_id)"

        comm_obj = self.pool.get('sondaggio.communication_batch')    
        parameter_obj = self.pool.get('sondaggio.parameter')    
        questionnaire_obj = self.pool.get('sondaggio.questionnaire')
    
        comm_ids = comm_obj.search(cr,uid,[('state','=','runnning')])
        mail_ids = []

        for comm in comm_obj.browse(cr,uid,comm_ids):
            email_parm = comm.email_parameter_name
            email_subject = comm.email_subject
            email_body = comm.email_body
            email_reply_to = comm.email_reply_to
            email_copy_to = comm.email_copy_to    
        
            for questionnaire in questionnaire_obj.browse(cr,uid,comm.waiting_ids):


                    base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url', default='', context=context)
                    if base_url:

			login = comm.login_user_id.login
			password = comm.login_user_id.password
                        base_url = 'http://fop.mierp.net/login?db=%s&login=%s&key=%s#action=questionnaire.ui&active_id=%s&active_code=%s' % (
                                cr.dbname,
                                login,
                                password,
                                questionnaire.id.id,
                                questionnaire.id.code
                        )
                    _logger.info('Base URL: %s' % base_url)

                    text_url = "<a href=\"%s\">%s</a>" % (base_url, base_url)

                    parameter_id = parameter_obj.search(cr, uid, [('questionnaire_id','=',questionnaire.id.id),('name','=',email_parm)])
                    if parameter_id:
                            data = parameter_obj.read(cr,uid,parameter_id,['value'])
                            email_value = data[0]['value']
                            mail_ids.append(mail_mail.create(cr, uid, {
                                    'email_from': email_reply_to,
                                    'email_to': email_value,
                                    'subject': email_subject,
                                    'body_html': '<pre>%s</pre><p>%s</p>' % (email_body,text_url)},
                                    context=context))
        mail_mail.send(cr, uid, mail_ids, context=context)
        _logger.info('%d Communication(s) sent.', len(mail_ids))
    
        return 0

communication_batch()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
