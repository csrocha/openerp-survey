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

from openerp.osv import fields,osv
from openerp import tools
from openerp.tools.translate import _
import logging
 
_logger = logging.getLogger(__name__)

class questionnaire_stats(osv.osv):
    _name = "sondaggio.questionnaire_stats"
    _description = "Questionnaire Stat"
    _auto = False
    _states_ = [
        ('draft','Draft'),
        ('cancelled','Cancelled'),
        ('waiting','Waiting'),
        ('in_process','In Process'),
        ('complete','Complete'),
        ('in_coding','In Coding'),
        ('validated','Validated'),
    ]
    _columns = {
        'survey_id': fields.many2one('sondaggio.survey', string='Survey', readonly=True, ondelete='cascade', required=True), 
        'state': fields.selection(_states_, "State"),
        'count': fields.float("Count"),
    }
    _order = 'survey_id asc, state asc'
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'sondaggio_questionnaire_stats')
        cr.execute("""
            CREATE OR REPLACE VIEW sondaggio_questionnaire_stats AS (
                SELECT
                    min(sondaggio_questionnaire.id) AS id,
                    sondaggio_questionnaire.survey_id AS survey_id,
                    sondaggio_questionnaire.state AS state,
                    COUNT(*) AS count
                FROM sondaggio_questionnaire
                GROUP BY survey_id, state
            )
        """)
 
questionnaire_stats()

class questionnaire_channel_stats(osv.osv):
    """

    Encuesta    Estados      Online Offline Personal Telefonico

    x           Borrador
    x           En Proceso
    x           Esperando
    x           Completo

    """
    _name = "sondaggio.questionnaire_channel_stats"
    _description = "Questionnaire Channel Stat"
    _auto = False
    _states_ = [
        ('draft','Draft'),
        ('cancelled','Cancelled'),
        ('waiting','Waiting'),
        ('in_process','In Process'),
        ('complete','Complete'),
        ('in_coding','In Coding'),
        ('validated','Validated'),
    ]
    _channels_ = [
        (u'online', 'online'),
        (u'personal', 'personal'),
        (u'telephonic', 'telephonic'),
        (u'offline', 'offline')
    ]
    _columns = {
        'survey_id': fields.many2one('sondaggio.survey', string='Survey', readonly=True, ondelete='cascade', required=True), 
        'state': fields.selection(_states_, "State"),
        'online': fields.float("Online"),
        'offline': fields.float("Offline"),
        'personal': fields.float("Personal"),
        'telephone': fields.float("Telephone"),
    }
    _order = 'survey_id asc, state asc'
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'sondaggio_questionnaire_stats')
        cr.execute("""
            CREATE OR REPLACE VIEW sondaggio_questionnaire_stats AS (
                SELECT
                    min(sondaggio_questionnaire.id) AS id,
                    sondaggio_questionnaire.state AS state,
                    COUNT(*) AS online
                    COUNT(*) AS offline
                    COUNT(*) AS personal
                    COUNT(*) AS telephone
                FROM sondaggio_questionnaire
                GROUP BY survey_id, state
            )
        """)
 
questionnaire_channel_stats()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
