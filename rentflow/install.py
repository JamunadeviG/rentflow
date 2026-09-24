import frappe


def after_install():
	categories = [
		{
			"category_name": "Power Drill",
			"daily_rate": 500,
			"deposit_amount": 2000
		},
		{
			"category_name": "Generator",
			"daily_rate": 1500,
			"deposit_amount": 5000
		},
		{
			"category_name": "Scaffold Tower Set",
			"daily_rate": 1000,
			"deposit_amount": 3000
		}
	]

	for category in categories:
		if not frappe.db.exists("Equipment Category", {"category_name": category["category_name"]}):
			doc = frappe.get_doc({
				"doctype": "Equipment Category",
				"category_name": category["category_name"],
				"daily_rate": category["daily_rate"],
				"deposit_amount": category["deposit_amount"]
			})
			doc.insert(ignore_permissions=True)

	if not frappe.db.exists("RentFlow Settings"):
		settings = frappe.get_doc({
			"doctype": "RentFlow Settings",
			"shop_name": "Anchor Point",
			"manager_email": "manager@example.com"
		})
		settings.insert(ignore_permissions=True)

	frappe.db.commit()
	frappe.msgprint("RentFlow default data created successfully.")