# import frappe
# from frappe.query_builder import DocType
# from datetime import date

# @frappe.whitelist()
# def get_overdue_returns():
#     RB = DocType("Rental Booking")
#     result = frappe.qb.from_(RB).select(RB.name, RB.customer_name, RB.end_date).where(RB.status=="Checked Out" and RB.end_date<date.today()).orderby(RB.end_date).run(as_dict=True)
#     return result

# @frappe.whitelist()
# def reassign_bookings(from_staff, to_staff):
#     try:
        