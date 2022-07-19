# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class period(models.Model):
    _name = 'elearn.period'
    _description = 'Periodo'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Nombre',
        required=True,
        default=lambda self: _('Periodo'),
        copy=False
    )

    
    vigente = fields.Boolean(
        string='Vigente',
    )

    
    fecha_inicio = fields.Date(
        string='Fecha inicio',
        default=fields.Date.context_today,
    )
    
    
    active = fields.Boolean(
        string='active',
        default = True
    )
    
    curse_ids = fields.One2many(
        string='Curso',
        comodel_name='elearn.curse',
        inverse_name='period_id',
    )
    
    
    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
    
        result = super(period, self).create(values)

        # 1 dominia
        #data = self.env['elearn.period'].search(domin)
        #plan itenra
        #data.write({'vigente':false})


    
        return result
    