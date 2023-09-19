from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class estate_Property(models.Model):
    _name = 'estate.estate.property'
    _description = 'Estate Properties'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'), ('canceled', 'Canceled')], default='new')
    postcode = fields.Char()
    description = fields.Text()
    date_availability = fields.Date(copy=False, default=(fields.Date.today() + relativedelta(days=+90)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
