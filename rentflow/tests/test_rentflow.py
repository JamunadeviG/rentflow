from frappe.tests.utils import FrappeTestCase

from rentflow.tests.test_factories import (
	make_category,
	make_staff,
	make_unit,
	make_booking
)


class TestRentFlow(FrappeTestCase):

	def setUp(self):
		# FrappeTestCase automatically rolls back database changes after each test,
		# so most manual tearDown() cleanup is unnecessary.
		pass

	def test_factories(self):
		category = make_category()
		staff = make_staff()
		unit = make_unit(category=category)
		booking = make_booking(unit=unit, handled_by=staff)

		self.assertIsNotNone(category.name)
		self.assertIsNotNone(staff.name)
		self.assertIsNotNone(unit.name)
		self.assertIsNotNone(booking.name)
		self.assertEqual(booking.docstatus, 0)
