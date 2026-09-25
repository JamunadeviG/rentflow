# Copyright (c) 2026, JamunadeviG and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document
from frappe.model.naming import getseries

class RentalInvoice(Document):
	pass
	
	# def before_save(self):
	# 	year = date.today().year
	# 	prefix = f"INV-{year}"
	# 	suffix = getseries(prefix, 5)
	# 	self.invoice_number = f"{prefix}-{suffix}"
	def before_save(self):
		self.invoice_number = self.name
