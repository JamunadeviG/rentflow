<!-- ----------B3 — Transactions & Commit Behavior------------ -->


<!-- Wrong Code -->
def validate(self):
    self.rental_total = sum(r.line_amount for r in self.items)
    self.save()
    unit = frappe.get_doc("Equipment Unit", self.items[0].equipment_unit)
    unit.current_status = "Rented"
    unit.save()


<!-- Corrected One -->
def validate(self):
    self.rental_total = sum(r.line_amount for r in self.items)
    unit = frappe.get_doc("Equipment Unit", self.items[0].equipment_unit)
    unit.current_status = "Rented"

REASON:
    * We should not use save() inside validate, because validate itself triggered after save. So, it will create a loop, like save --> validate --> save --> validate.



<!-- -------------B4 — Concurrency, One Question-------------- -->

In README_internals.md: why would two staff members confirming the same booking at once trigger a "Document has been modified after you have opened it" error, and how does Frappe prevent the silent overwrite?

REASON:
I tried to update a same document in different browser with different users it results in """Error: RB-2026-0008 (Rental Booking) has been modified after you have opened it (2026-09-23 14:58:35.478517, 2026-09-23 14:58:36.707316). Please refresh to get the latest document.""". As we can clearly see in the error itself it mentioned the timestamp of the record I gave save earlier, it throws this error with last_modified _on



<!-- -------------------E3 — frappe.db.get_value vs frappe.get_doc---------------------- -->

I would use frappe.db.get_value() when I only need the low_availability_threshold value.

threshold = frappe.db.get_value("RentFlow Settings", None, "low_availability_threshold")

frappe.get_doc() loads complete RentFlow Settings doc, which is unnecessary when I need only one field. frappe.db.get_value() gets only the required value and avoids loading the complete doc, and it is the better choice to go with.



<!-- --------------------------Group J — Print Format------------------------- -->

`frappe.get_all()` in Jinja directly fetches data while printing, which can make the template messy.
Using `before_print()` prepares the data first, so Jinja only displays it and stays simple.
