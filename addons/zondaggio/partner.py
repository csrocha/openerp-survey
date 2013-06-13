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

import netsvc
from osv import osv, fields
from openerp.tools.translate import _

class partner(osv.osv):
    """"""
    _name = 'res.partner'
    _inherit = [ _name ]

    def generate_questions(self, cr, uid, ids, context=None):
        """
        Call to survey to generate main answer entries.
        """
        context = context or {}

        survey_id = context.get('survey_id',None)

        if survey_id is None:
            return True

        survey_obj = self.pool.get('sondaggio.survey')
        model_obj = self.pool.get('ir.model.data')

        if survey_obj.browse(cr, uid, survey_id).state != 'published':
            raise osv.except_osv(_('Error'), _('You can load answer in published state, not in other'))

        r = survey_obj.generate_questions(cr, uid, [survey_id], {'respondent_ids': ids, 'pollster_id': uid})
        r = r[0] if r else False;

        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Questionnaire',
            'view_type': 'form,tree',
            'view_mode': 'form',
            'res_model': 'sondaggio.questionnaire',
            'res_id': r,
            'context': context,
        }

partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
