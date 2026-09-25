# Copyright (c) 2026, JamunadeviG and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries


class EquipmentCategory(Document):
	def autoname(self):
		prefix = self.category_name
		suffix = getseries(prefix, 4)
		self.name = f"{prefix}-{suffix}"