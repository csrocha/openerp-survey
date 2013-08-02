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
    _inherit = 'sondaggio.communication_batch'

    def do_publish(self, cr, uid, ids=None,context=None):
        """Completa la lista de waiting_questionnaire_ids a partir de los questionnaire_ids que hay en survey_id. Cambia a estado running."""
        raise NotImplementedError


    def send_mails(self, cr, uid, ids, context=None):
        """Envia un mail por cada waiting_questionnaires_ids usando los datos de la comunicación (email, subject, body, reply_to, etc) una vez enviado se borra de waiting y pasa a done_questionnaire_ids. Si no hay más emails en waiting se cambia a estado "done"."""

        communication_batch_obj = self.pool.get('sondaggio.communication_batch')
	parameter_obj = self.pool.get('sondaggio.parameter')	

	import pdb;pdb.set_trace()
	comm_ids = communication_batch_obj.search(cr, uid, [('state', '=', 'Waiting')])
	for communication in communication_batch_obj.browse(cr,uid,comm_ids,context=context):
		if communication.email_parameter_name:
			parameter_code = communication.email_parameter_name
			parameter_id = parameter_obj.search(cr,uid,[('name','=',parameter_code)])
			if parameter_id:
				for parameter in parameter_obj.browse(cr,uid,parameter_id,context=context): 
					parameter_value = parameter.value
									
        return None


communication_batch()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
