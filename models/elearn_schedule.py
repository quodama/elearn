# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class schedule(models.Model):
    _name = 'elearn.schedule'
    _description = 'Horario'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Horario',
        required=True,
        default=lambda self: _('Horario'),
        copy=False
    )
    
    schedule_curse = fields.Char(
        string='Horas',
    )

    sequence = fields.Integer(
        string='sequence',
        default = 16
    )
    
    curse_ids = fields.One2many(
        string='Curso',
        comodel_name='elearn.curse',
        inverse_name='schedule_id',
    )
    active = fields.Boolean(
        string='active',
        default = True
    )
