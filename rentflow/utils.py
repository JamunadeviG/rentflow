import frappe


def get_shop_name():
    return frappe.db.get_single_value(
        "RentFlow Settings",
        "shop_name"
    ) or "Anchor Point"