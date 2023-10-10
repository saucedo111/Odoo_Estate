from odoo import models, fields


class estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True, default='House')

    _sql_constraints = [
        ('check_name', 'UNIQUE (name)', 'The name must be unique')
    ]
