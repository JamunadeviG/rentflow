# Copyright (c) 2026, JamunadeviG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class RentalBooking(Document):

	def validate(self):
		self.validate_dates()
		self.check_for_duplicate()
		self.cal_line_days()
		self.cal_line_amount()
		self.cal_damage_fee()
		self.cal_rental_damage_final_total()

	def before_submit(self):
		if(self.status != "Confirmed" or self.deposit_collected <= 0):
			frappe.throw("Deposit has to be greater than 0 and status has to be Confirmed")

	def on_submit(self):
		for row in self.items or []:
			frappe.db.set_value("Equipment Unit", row.equipment_unit, 'current_status', "Reserved")
		self.create_rental_invoice()
		self.enqueue_booking_confirmation_email()

	def on_cancel(self):
		self.status = "Cancelled"
		for row in self.items or []:
			frappe.db.set_value("Equipment Unit", row.equipment_unit, 'current_status', "Available")


	def validate_dates(self):
		start_date = getdate(self.start_date)
		end_date = getdate(self.end_date)
		if start_date > end_date:
			frappe.throw("Start Date must be less than or equal to End Date. Please reselect the dates.")


	def check_for_duplicate(self):
		seen = {}
		for row in self.items or []:
			if not row.equipment_unit:
				continue
			if row.equipment_unit in seen:
				frappe.throw(f"Conflict occurred. Equipment unit '{row.equipment_unit}' cannot be added more than once.")
			seen[row.equipment_unit] = True


	def cal_line_days(self):
		start_date = getdate(self.start_date)
		end_date = getdate(self.end_date)
		line_days = (end_date - start_date).days + 1

		for row in self.items or []:
			row.line_days = line_days


	def cal_line_amount(self):
		for row in self.items or []:
			if not row.category:
				row.daily_rate = 0
				row.line_amount = 0
				continue
			daily_rate = frappe.db.get_value("Equipment Category", row.category, "daily_rate")
			if daily_rate is None:
				frappe.throw(f"Daily Rate is not set for Equipment Category '{row.category}'.")
			row.daily_rate = daily_rate
			row.line_amount = row.line_days * row.daily_rate

	def cal_damage_fee(self):
		grade = {"New": 5, "Good": 4, "Fair": 3, "Poor": 2, "Damaged": 1}
		for row in self.items or []:
			g1 = row.checkout_condition_grade
			g2 = row.checkin_condition_grade
			rg = grade[g1] - grade[g2]
			damage_fee_per_grade_drop = frappe.db.get_single_value("Rentflow Settings", 'damage_fee_per_grade_drop')
			row.damage_fee = damage_fee_per_grade_drop * rg

	def cal_rental_damage_final_total(self):
		rent = 0
		damage = 0
		for row in self.items or []:
			rent += row.line_amount
			damage += row.damage_fee

		self.rental_total = rent
		self.damage_total = damage
		self.final_amount = rent + damage


	def create_rental_invoice(self):

		existing_invoice = frappe.db.exists(
			"Rental Invoice",
			{"rental_booking": self.name}
		)

		if existing_invoice:
			return

		invoice = frappe.get_doc({
			"doctype": "Rental Invoice",
			"rental_booking": self.name,
			"customer_name": self.customer_name,
			"invoice_date": frappe.utils.today(),
			"rental_amount": self.rental_total,
			"damage_amount": self.damage_total,
			"total_amount": self.final_amount,
			"payment_status": "Unpaid"
		})

		invoice.insert(ignore_permissions=True)


	def enqueue_booking_confirmation_email(self):

		frappe.enqueue(
			"rentflow.rentflow.doctype.rental_booking.rental_booking.send_booking_confirmed_email",
			booking_name=self.name,
			queue="short",
			enqueue_after_commit=True
		)


def send_booking_confirmed_email(booking_name):

	booking = frappe.get_doc(
		"Rental Booking",
		booking_name
	)

	customer_email = frappe.db.get_value(
		"Customer",
		booking.customer,
		"email"
	)

	if not customer_email:
		return

	frappe.sendmail(
		recipients=[customer_email],
		subject=f"Rental Booking {booking.name} Confirmed",
		message=f"""
			<p>Hello {booking.customer},</p>
			<p>Your rental booking <b>{booking.name}</b> has been confirmed.</p>
			<p><b>Rental Amount:</b> ₹{booking.rental_total}</p>
			<p><b>Damage Amount:</b> ₹{booking.damage_total}</p>
			<p><b>Total Amount:</b> ₹{booking.final_amount}</p>
			<p>Thank you for choosing RentFlow.</p>
		"""
	)