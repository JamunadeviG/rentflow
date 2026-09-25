# Copyright (c) 2026, JamunadeviG and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries

class EquipmentUnit(Document):
	def autoname(self):
		prefix = self.category[:3].upper()
		suffix = getseries(prefix, 5)
		self.name = f"{prefix}-{suffix}"