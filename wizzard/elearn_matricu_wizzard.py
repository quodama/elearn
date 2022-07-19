# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ElearnMatricuWizzard(models.TransientModel):
    _name = 'elearn.matricu.wizzard'
    _description = 'Wizzard Matriculacion'

    
    curse_id = fields.Many2one(
        string='Curso',
        comodel_name='elearn.curse',
        ondelete='restrict',
    )

    estudiante_id = fields.Many2one(
        string='Estudiante',
        comodel_name='res.partner',
        ondelete='restrict',
    )

    
    only_student_ids = fields.One2many(
        string='Only Student',
        comodel_name='res.partner',
        compute='_compute_only_student_ids' 
    )
        
    @api.depends('curse_id')    
    def _compute_only_student_ids(self):
        for record in self:
            domain=[("category_id.id","=",self.env.ref('elearn.category_res_partnet_student').id)]
            record.only_student_ids = self.env['res.partner'].search(domain)
        
        
        
    

    def accion_matricular(self):

        values ={
            'curse_id':self.curse_id.id,
            'actor_respartner_id':self.estudiante_id.id,
            'category_elaran_id':self.env.ref('elearn.category_res_partnet_student').id
        } 

        self.env['elearn.curse.res.partner'].create(values)
    

    
