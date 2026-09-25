import frappe


def make_category(**kwargs):
	data = {
		"doctype": "Equipment Category",
		"category_name": "Test Category",
		"description": "Test equipment category",
		"daily_rate": 500,
		"deposit_amount": 1000
	}
	data.update(kwargs)
	return frappe.get_doc(data).insert()


def make_staff(**kwargs):
	data = {
		"doctype": "Yard Staff",
		"staff_name": "Test Staff",
		"employee_id": "TEST-001",
		"phone": "9999999999",
		"email": "test@example.com",
		"role": "Front Desk",
		"status": "Active"
	}
	data.update(kwargs)
	return frappe.get_doc(data).insert()


def make_unit(**kwargs):
	category = kwargs.pop("category", None)

	if not category:
		category = make_category()

	data = {
		"doctype": "Equipment Unit",
		"unit_code": "TEST-UNIT-001",
		"category": category.name,
		"condition_grade": "New",
		"current_status": "Available",
		"purchase_value": 10000,
		"is_active": 1
	}
	data.update(kwargs)
	return frappe.get_doc(data).insert()


def make_booking(**kwargs):
	unit = kwargs.pop("unit", None)
	staff = kwargs.pop("handled_by", None)

	if not unit:
		unit = make_unit()

	if not staff:
		staff = make_staff()

	data = {
		"doctype": "Rental Booking",
		"customer_name": "Test Customer",
		"customer_phone": "9999999999",
		"customer_email": "customer@example.com",
		"start_date": "2026-10-01",
		"end_date": "2026-10-03",
		"handled_by": staff.name,
		"deposit_collected": 1000,
		"status": "Confirmed",
		"items": [
			{
				"equipment_unit": unit.name,
				"checkout_condition_grade": "New"
			}
		]
	}
	data.update(kwargs)
	return frappe.get_doc(data).insert()
