# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Respartner(models.Model):
    _inherit = 'res.partner'

    
    curses_elearn_ids = fields.One2many(
        string='Curses Elearn',
        comodel_name='elearn.curse.res.partner',
        inverse_name='actor_respartner_id',
    )

    
    @api.model
    def create(self, values):
        """
            Create a new record for a model Respartner
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
    
        result = super(Respartner, self).create(values)

        if('curse_id' in self.env.context):
            newValues={
                'curse_id':self.env.context['curse_id'],
                'actor_respartner_id':result.id,
                'category_elaran_id':self.env.context['default_category_id'][0],
            }
            self.env['elearn.curse.res.partner'].create(newValues)
    
        return result
    
    

    


