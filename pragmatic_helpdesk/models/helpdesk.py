# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import models, fields, api, tools
import logging
from datetime import datetime as dt
import datetime
import time
from openerp.exceptions import ValidationError
from openerp.osv import fields as fieldsOld, osv, orm

_logger = logging.getLogger(__name__)


    
class PragmaticTarea(models.Model):
    _inherit =  ['project.task']
    meeting_id = fields.Many2one('calendar.event', string='Reunión')

class PragmaticReunion(models.Model):
    _inherit =  ['calendar.event']
    
    project_id = fields.Many2one(string='Proyecto')
    task_ids = fields.One2many('project.task','meeting_id',string='Compromisos')
    goals = fields.Text(string='Objetivos')
    development = fields.Text(string='Desarrollo')
    #description = fields.Text(string='Temas a tratar')


class project(osv.Model):
    _inherit = "project.project"

    
    def _meeting_count(self, cr, uid, ids, field_name, arg, context=None):
        Meeting = self.pool['calendar.event']
        return {
            project_id: Meeting.search_count(cr,uid, [('project_id', '=', project_id)], context=context)
            for project_id in ids
        }

    def _meeting_needaction_count(self, cr, uid, ids, field_name, arg, context=None):
        """Meeting = self.pool['calendar.event']
        res = dict.fromkeys(ids, 0)
        projects = Meeting.read_group(cr, uid, [('project_id', 'in', ids), ('message_needaction', '=', True)], ['project_id'], ['project_id'], context=context)
        res.update({project['project_id'][0]: int(project['project_id_count']) for project in projects})
        return res"""
        return 0

    _columns = {
        'meeting_count': fieldsOld.function(_meeting_count, type='integer', string="Reuniones",),
        'meeting_ids': fieldsOld.one2many('calendar.event', 'project_id', string="Reuniones",),
        'meeting_needaction_count': fieldsOld.function(_meeting_needaction_count, type='integer', string="Reuniones",),
        'use_meetings': fieldsOld.boolean("Usar reuniones"),
        'label_meeting': fieldsOld.char('Usar reuniones como'),
    }

    _defaults = {
        'use_meetings': False,
        'label_meeting': 'Reuniones',
    }

    def on_change_use_tasks_or_issues(self, cr, uid, ids, use_tasks, use_issues, use_meetings, context=None):
        values = {}
        if use_tasks and not use_issues and not use_meetings:
            values['alias_model'] = 'project.task'
        elif not use_tasks and use_issues and not use_meetings:
            values['alias_model'] = 'project.issue'
        elif not use_tasks and not use_issues and use_meetings:
            values['alias_model'] = 'calendar.event'
        return {'value': values}


class PragmaticReclamo(models.Model):
    _inherit =  ['project.issue']
    

    dias_limite = fields.Integer(string='Días para el vencimiento', compute='_compute_dias_vencimiento')
    
    @api.multi
    @api.depends('date_deadline')
    def _compute_dias_vencimiento(self):
        for reclamo in self:  
            if reclamo.date_deadline:
                fmt = '%Y-%m-%d'   
                d1 = dt.strptime(time.strftime('%Y-%m-%d'), fmt)
                d2 = dt.strptime(reclamo.date_deadline, fmt)
                reclamo.dias_limite = str((d2-d1).days) 


class PragmaticEncabezado(models.Model):
    _inherit = 'res.company'
    _description = 'Encabezado reporte'  
    encabezado =fields.Binary(string='Imagen encabezado')
    pie_pagina =fields.Binary(string='Pie de pagina')
            
    
    
   
