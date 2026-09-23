import frappe
from frappe import _
from frappe.query_builder import DocType
from datetime import date



# ---------------B1 — Query Builder----------------
@frappe.whitelist()
def get_overdue_returns():
    RB = DocType("Rental Booking")
    result = frappe.qb.from_(RB).select(RB.name, RB.customer_name, RB.end_date).where(RB.status=="Checked Out" and RB.end_date<date.today()).orderby(RB.end_date).run(as_dict=True)
    return result


# ---------------B2 — Transactions & Commit Behavior----------------
@frappe.whitelist()
def reassign_bookings(from_staff, to_staff):
    try:
        frappe.db.sql(
            """
            UPDATE `tabRental Booking`
            SET handled_by = %s
            WHERE handled_by = %s
              AND status = 'Confirmed'
            """,
            (to_staff, from_staff)
        )
        frappe.db.commit()
        return "Success"

    except Exception:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Booking Reassignment Failed")
        raise


# ---------------D1 — Permission Matrix & Sharing----------------
# for D1 permission_query_conditions
@frappe.whitelist()
def share_booking(booking_name, user_email):
    if not booking_name or not user_email:
        frappe.throw("Both booking name and user email are required.")

    try:
        frappe.share.add(doctype="Rental Booking", name=booking_name, user=user_email, read=1)
        return {
            "status": "success",
            "message": f"Booking '{booking_name}' shared with {user_email} for read access."
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Share Booking Error")
        frappe.throw(f"Failed to share booking: {e}")


# --------------D2 — Row-Level Filtering & Data Leaks-----------------
def rental_booking_query(user):
    roles = frappe.get_roles(user)

    if "Administrator" in roles:
        return ""

    if "Inspector" in roles:
        yard_staff = frappe.db.get_value(
            "Yard Staff",
            {"user": user},
            "name"
        )

        if not yard_staff:
            return "1 = 0"

        return f"`tabRental Booking`.`handled_by` = '{yard_staff}'"

    return ""


@frappe.whitelist()
def safe_bookings():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    bookings = frappe.get_list(
        "Rental Booking",
        fields=[
            "name",
            "customer",
            "customer_phone",
            "customer_email",
            "handled_by"
        ]
    )

    if "Rentflow Manager" not in roles:
        for booking in bookings:
            booking.pop("customer_phone", None)
            booking.pop("customer_email", None)

    return bookings
