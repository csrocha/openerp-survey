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

        survey_obj = self.pool.get('survey_methodology.survey')
        model_obj = self.pool.get('ir.model.data')

        if survey_obj.browse(cr, uid, survey_id).state != 'published':
            raise osv.except_osv(_('Error'), _('You can load answer in published state, not in other'))

        r = survey_obj.generate_questions(cr, uid, [survey_id], {'respondent_ids': ids, 'pollster_id': uid})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Load Answers',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'survey_methodology.answer',
            'view_id': model_obj.get_object_reference(cr, uid, 'survey_methodology', 'view_survey_methodology_answer_tree_edit')[1],
            'domain': [('respondent_id','in',ids),('pollster_id','=',uid),('survey_id','=',survey_id)],
            'context': context,
        }

partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
