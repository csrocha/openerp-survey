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

class answer(osv.osv):
    """"""
    _name = 'survey_methodology.answer'
    _description = 'answer'

    def _get_progress(self, cr, uid, ids, name, attrs, context=None):
        """"""
        raise NotImplementedError

    _states_ = [
    ]

    _columns = {
        'name': fields.char(string='name', required=True),
        'responder_id': fields.many2one('res.partner', string='responder_id', required=True),
        'surveyor_id': fields.many2one('res.partner', string='surveyor_id'),
        'progress': fields.float(string='progress'),
        'question_id': fields.many2one('survey_methodology.question', string='question_id', required=True), 
        'survey_id': fields.many2one('survey_methodology.survey', string='survey_id', required=True), 
    }

    _defaults = {
    }

    def is_valid(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError


answer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
