# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CurseResPartner(models.Model):
    _name = 'elearn.curse.res.partner'
    _description = 'Descomposicion de una realicion many2many'

    
    curse_id = fields.Many2one(
        string='Curso',
        comodel_name='elearn.curse',
        ondelete='restrict',
    )

    
    actor_respartner_id = fields.Many2one(
        string='Actor',
        comodel_name='res.partner',
        ondelete='restrict',
    )

    category_elaran_id = fields.Many2one(
        string='Rol',
        comodel_name='res.partner.category',
        ondelete='restrict',
        required=True
    )
    
    

class Curse(models.Model):
    _name = 'elearn.curse'
    _description = 'curse'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Curso',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    period_id = fields.Many2one(
       string='Periodo',
       comodel_name='elearn.period',
       ondelete='restrict',
       required=True
   )

    schedule_id = fields.Many2one(
       string='Horario',
       comodel_name='elearn.schedule',
       ondelete='restrict',
   )

    actor_ids = fields.One2many(
       string='Actor',
       comodel_name='elearn.curse.res.partner',
       inverse_name='curse_id',
   )

   #Estudiante
    #método que permite obtener una lista de actores de 
    #tipo estudiante
    student_ids = fields.One2many(
        string='Estudiantes',
        comodel_name='res.partner',
        compute='_compute_actor_ids' 
    )

    #profesor
    profesor_ids = fields.One2many(
        string='Profesores',
        comodel_name='res.partner',
        compute='_compute_actor_ids' 
    )

    #padre
    padre_ids = fields.One2many(
        string='Padres',
        comodel_name='res.partner',
        compute='_compute_actor_ids' 
    )

    #Crear relación a nivel del ORM con la finalidad 
    # de crear consulta por tipo de Actores 

    #Contador de Estudiantes 
    count_student = fields.Integer(
        string='Contador estudiantes',
        compute='_compute_count_student'
    )

    count_profesor = fields.Integer(
        string='Contador profesores',
        compute='_compute_count_profesor'
    )

    count_padre = fields.Integer(
        string='Contador padres',
        compute='_compute_count_padre'
    )

    #Estado del curso

    state = fields.Selection(
        string='Estado',
        selection=[
            ('draft', 'Borrador'), 
            ('planning', 'Planificado'),
            ('doing', 'Ejecutando'),
            ('close', 'Cerrado'),
            ],
        default='draft',
        require=True,
    )


    @api.depends('student_ids')
    def _compute_count_student(self):
        for record in self:
            record.count_student =len(record.student_ids)

    @api.depends('profesor_ids')
    def _compute_count_profesor(self):
        for record in self:
            record.count_profesor =len(record.profesor_ids)     

    @api.depends('padre_ids')
    def _compute_count_padre(self):
        for record in self:
            record.count_padre =len(record.padre_ids)                 

    @api.depends('actor_ids')
    def _compute_actor_ids(self):
        for record in self:
            # notacion polaca
            # x = 2 +3  notacion entre signos
            # x = + 2 3 NOTACION entre polaca
            domain = [('category_elaran_id','=', self.env.ref('elearn.category_res_partnet_student').id ),('curse_id','=',record.id)]
            #   select actor_respartner_id  from elearn_curse_res_partner ecrp where curse_id =1 and category_elaran_id =2
            data_ids = self.env['elearn.curse.res.partner'].search(domain)


            students = []
            for data in data_ids:
                students.append(data.actor_respartner_id.id)

            #select * from res_partner rp  where id in (8,10)
            record.student_ids = self.env['res.partner'].browse(students)

            #Profes
            domain = [('category_elaran_id','=', self.env.ref('elearn.category_res_partnet_profesor').id ),('curse_id','=',record.id)]
            #   select actor_respartner_id  from elearn_curse_res_partner ecrp where curse_id =1 and category_elaran_id =2
            data_ids = self.env['elearn.curse.res.partner'].search(domain)

            profes = []
            for data in data_ids:
                profes.append(data.actor_respartner_id.id)

            #select * from res_partner rp  where id in (8,10)
            record.profesor_ids = self.env['res.partner'].browse(profes) 
            #
            #Padres
            domain = [('category_elaran_id','=', self.env.ref('elearn.category_res_partnet_padre').id ),('curse_id','=',record.id)]
            #   select actor_respartner_id  from elearn_curse_res_partner ecrp where curse_id =1 and category_elaran_id =2
            data_ids = self.env['elearn.curse.res.partner'].search(domain)

            padres = []
            for data in data_ids:
                padres.append(data.actor_respartner_id.id)

            #select * from res_partner rp  where id in (8,10)
            record.padre_ids = self.env['res.partner'].browse(padres) 
            #

    """ @api.depends('actor_ids')
    def _compute_profesor_ids(self):
        for record in self:
            # notacion polaca
            # x = 2 +3  notacion entre signos
            # x = + 2 3 NOTACION entre polaca
            domain = [('category_elaran_id','=', self.env.ref('elearn.category_res_partnet_profesor').id ),('curse_id','=',record.id)]
            #   select actor_respartner_id  from elearn_curse_res_partner ecrp where curse_id =1 and category_elaran_id =2
            data_ids = self.env['elearn.curse.res.partner'].search(domain)

            profes = []
            for data in data_ids:
                profes.append(data.actor_respartner_id.id)

            #select * from res_partner rp  where id in (8,10)
            record.student_ids = self.env['res.partner'].browse(profes)    """     

    def action_view_student(self):
        
        domain = [('id','in',self.student_ids.ids)]
        action ={
            'type':'ir.actions.act_window',
            'name':'Estudiantes matriculados',
            'res_model':'res.partner',
            'view_mode':'kanban,tree,form',
            'target':'current',
            'domain':domain,
            'context':{
                'default_category_id':[self.env.ref('elearn.category_res_partnet_student').id], #importante el dafault agregar al campo
                'curse_id':self.id
                },
        } 
        return action;

    def action_view_profesor(self):
        
        domain2 = [('id','in',self.profesor_ids.ids)]
        action2 ={
            'type':'ir.actions.act_window',
            'name':'Profesores asignados',
            'res_model':'res.partner',
            'view_mode':'kanban,tree,form',
            'target':'current',
            'domain':domain2,
            'context':{},
        } 
        return action2;

    def action_view_padre(self):
        
        domain2 = [('id','in',self.padre_ids.ids)]
        action2 ={
            'type':'ir.actions.act_window',
            'name':'Padres de Familia',
            'res_model':'res.partner',
            'view_mode':'kanban,tree,form',
            'target':'current',
            'domain':domain2,
            'context':{},
        } 
        return action2;    

    
    count_attachment = fields.Integer(
        string='Count Attachment',
        compute='_compute_count_attachment' 
    )
        
        
    def _compute_count_attachment(self):
        for record in self:    
            domain = [('res_model','=',self._name), ('res_id','=',self.id)]            
            count = self.env['ir.attachment'].search_count(domain)
            record.count_attachment = count
        

    def action_view_attachment(self):
        domain = [('res_model','=',self._name), ('res_id','=',self.id)]
        action ={
            'type':'ir.actions.act_window',
            'name':'Documentos',
            'res_model':'ir.attachment',
            'view_mode':'kanban,tree,form',
            'target':'current',
            'domain':domain,
            'context':{
                'default_res_model':self._name,
                'default_res_id':self.id
                },
        } 
        return action
    
    """ res_model_id = fields.Many2one(
        'ir.model', 
        'Document Model',
        index=True, 
        ondelete='cascade'
    )

    res_model = fields.Char(
        'Related Document Model',
        index=True, 
        related='res_model_id.model', 
        store=True )

    res_id = fields.Many2oneReference(
        string='Related Document ID', 
        index=True, 
        model_field='res_model'
    )
 """
    referense_id = fields.Reference(       
        string='Driver Related To',
        ondelete='restrict',
        index=True, 
        selection='_selection_target_model'
     )
    
    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env['ir.model'].search([])]    
    
    def action_matricula(self):
        action ={
            'type':'ir.actions.act_window',
            'name':'Matriculación',
            'res_model':'elearn.matricu.wizzard',
            'view_mode':'form',
            'target':'new',
            'res_id':0,
            'context':{
                'default_curse_id':self.id,
                },
        } 
        return action



   
   