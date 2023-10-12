from odoo import models, fields


class estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True, default='House')
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence')

    _sql_constraints = [
        ('check_name', 'UNIQUE (name)', 'The name must be unique')
    ]
