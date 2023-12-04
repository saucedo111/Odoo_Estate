from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstate, cls).setUpClass()
        cls.properties = cls.env['estate.property'].create({
            'name': 'Tprop',
            'expected_price': 100
        })
        cls.partners = cls.env['res.partner'].create({
            'name': 'Tbuyer'
        })
        cls.offers = cls.env['estate.property.offer'].create({
            'partner_id': cls.partners.id,
            'property_id': cls.properties[0].id,
            'price': 90
        })

    def test_action_sell(self):
        with self.assertRaises(UserError):
            self.properties.action_sold()
        self.offers.action_accept()
        self.properties.action_sold()
        self.assertEqual(self.properties[0].state, 'sold')
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'name': 'Toffer2',
                'partner_id': self.partners.id,
                'property_id': self.properties[0].id,
                'price': 95
            })

    # def test_form(self):






