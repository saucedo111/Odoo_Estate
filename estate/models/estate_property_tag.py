from odoo import models, fields


class estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(help='Choose your color, enter an integer between 0 and 11, 0 is none', default=0)

    _sql_constraints = [
        ('check_name', 'UNIQUE (name)', 'The name must be unique')
    ]
