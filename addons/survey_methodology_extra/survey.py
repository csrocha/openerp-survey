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

class survey(osv.osv):
    """"""
    _name = 'survey_methodology.survey'
    _inhere = [ _name ]

    def generate_sample(self, cr, uid, ids, context=None):
        """"""
        context = context or {}
        partner_obj = self.pool.get('res.partner')

        for survey in self.browse(cr, uid, ids, context):
            sample_size = survey.sample_size
            sample_filter = survey.partner_filter
            partner_ids = partner_obj.search(cr, uid, sample_filter)
            sample_ids = random.sample(partner_ids, samples_size)
            self.write(cr, uid, survey.id, {'partner_ids': sample_ids })

        return True

    def generate_questions(self, cr, uid, ids, context=None):
        """"""
        context = context or {}
        for survey in self.browse(cr, uid, ids, context):
            pass
        return True

survey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
