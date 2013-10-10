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
        ('rejected','Rejected'),
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
                    min(A.id) AS id,
                    A.survey_id AS survey_id,
                    A.state AS state,
                    COUNT(*) AS count
                FROM sondaggio_questionnaire AS A
                GROUP BY A.survey_id, A.state
            )
        """)
 
questionnaire_stats()

class estrato_stats(osv.osv):
    _name = "sondaggio.estrato_stats"
    _description = "Questionnaire Stat"
    _auto = False
    _states_ = [
        ('draft','Draft'),
        ('cancelled','Cancelled'),
        ('waiting','Waiting'),
        ('in_process','In Process'),
        ('complete','Complete'),
        ('in_coding','In Coding'),
        ('rejected','Rejected'),
        ('validated','Validated'),
    ]
    _columns = {
        'name': fields.integer('Estrato', readonly=True), 
        'survey_id': fields.many2one('sondaggio.survey', 'Survey ID', readonly=True), 
        'total': fields.integer('Total', readonly=True),
        'total_ver': fields.integer('Total Verificado', readonly=True),
        'total_muestra': fields.integer('Total Muestra', readonly=True),
        'pendiente': fields.integer('Pendiente', readonly=True),
        'channel_undefined': fields.integer('Undefined', readonly=True),
        'channel_online': fields.integer('Online', readonly=True),
        'channel_offline': fields.integer('Offline', readonly=True),
        'channel_telephonic': fields.integer('Telephonic', readonly=True),
        'channel_personal': fields.integer('Personal', readonly=True),
        'state_draft': fields.integer('Draft', readonly=True),
        'state_cancelled': fields.integer('Cancelled', readonly=True),
        'state_waiting': fields.integer('Waiting', readonly=True),
        'state_in_process': fields.integer('In Process', readonly=True),
        'state_complete': fields.integer('Complete', readonly=True),
        'state_in_coding': fields.integer('In Coding', readonly=True),
        'state_rejected': fields.integer('Rejected', readonly=True),
        'state_validated': fields.integer('Validated', readonly=True),
    }
    _order = 'name asc'
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'sondaggio_estrato_stats')
        cr.execute("""
            CREATE OR REPLACE VIEW sondaggio_estrato_stats AS (
                SELECT
                   E.id as id,
                   E.name::int as name,
                   E.survey_id as survey_id,
                   COUNT(*) as total,
                   E.tam_muestra as total_muestra,
                   E.tam_muestra - SUM(CASE WHEN Q.state in  ('draft', 'waiting', 'in_process', 'cancelled', 'rejected') THEN 0 ELSE 1 END) as pendiente,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        NULLIF(par_fecha_ver,'') is NULL) as total_ver,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        channel is NULL) as channel_undefined,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        channel='online') as channel_online,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        channel='offline') as channel_offline,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        channel='telephonic') as channel_telephonic,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        channel='personal') as channel_personal,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='draft') as state_draft,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='cancelled') as state_cancelled,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='waiting') as state_waiting,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='in_process') as state_in_process,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='complete') as state_complete,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='in_coding') as state_in_coding,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='rejected') as state_rejected,
                   (SELECT count(*) FROM sondaggio_questionnaire AS P WHERE
                        P.survey_id=E.survey_id AND
                        NULLIF(P.par_estrato_f,'')::int=NULLIF(E.name,'')::int AND
                        state='validated') as state_validated
                FROM sondaggio_estrato AS E
                     LEFT JOIN sondaggio_questionnaire AS Q
                   ON (NULLIF(E.name,'')::int = NULLIF(Q.par_estrato_f,'')::int)
                   GROUP BY E.id
            )
        """)
 
estrato_stats()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
