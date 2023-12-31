from odoo import models, fields


class ResUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Properties',
                                   domain=['|', ('state', '=', 'offer_received'),
                                           ('state', '=', 'new')])
