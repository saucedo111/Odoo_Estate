from odoo import models, fields


class estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE (name)', 'The name must be unique')
    ]
