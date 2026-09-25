# import frappe
# from frappe.utils import getdate, date_diff


# def execute(filters=None):
# 	filters = filters or {}
# 	columns = get_columns()
# 	data = get_data(filters)
# 	return columns, data, None, get_chart(data), get_report_summary(data)


# def get_columns():
# 	return [
# 		{"label": "Category", "fieldname": "category", "fieldtype": "Link", "options": "Equipment Category", "width": 180},
# 		{"label": "Total Units", "fieldname": "total_units", "fieldtype": "Int", "width": 110},
# 		{"label": "Days Rented", "fieldname": "days_rented", "fieldtype": "Int", "width": 110},
# 		{"label": "Utilization %", "fieldname": "utilization", "fieldtype": "Percent", "width": 110},
# 		{"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 120},
# 		{"label": "Damage Incidents", "fieldname": "damage_incidents", "fieldtype": "Int", "width": 130}
# 	]


# def get_data(filters):
# 	from_date = getdate(filters.get("from_date"))
# 	to_date = getdate(filters.get("to_date"))

# 	if not from_date or not to_date:
# 		frappe.throw("Please select From Date and To Date.")

# 	if from_date > to_date:
# 		frappe.throw("From Date cannot be greater than To Date.")

# 	category_filter = filters.get("category")

# 	unit_filters = {"is_active": 1}

# 	if category_filter:
# 		unit_filters["category"] = category_filter

# 	units = frappe.get_list(
# 		"Equipment Unit",
# 		fields=["name", "category"],
# 		filters=unit_filters
# 	)

# 	category_data = {}

# 	for unit in units:
# 		category = unit.category

# 		if category not in category_data:
# 			category_data[category] = {
# 				"total_units": 0,
# 				"days_rented": 0,
# 				"revenue": 0,
# 				"damage_incidents": 0
# 			}

# 		category_data[category]["total_units"] += 1

# 	if not units:
# 		return []

# 	bookings = frappe.get_list(
# 		"Rental Booking",
# 		fields=["name", "start_date", "end_date", "status"],
# 		filters={
# 			"docstatus": 1,
# 			"status": ["in", ["Confirmed", "Checked Out", "Returned", "Invoiced", "Closed"]],
# 			"start_date": ["<=", to_date],
# 			"end_date": [">=", from_date]
# 		}
# 	)

# 	if not bookings:
# 		return build_data(category_data)

# 	booking_names = [booking.name for booking in bookings]

# 	items = frappe.get_list(
# 		"Booking Item",
# 		fields=["parent", "equipment_unit", "line_days", "line_amount", "damage_fee"],
# 		filters={"parent": ["in", booking_names]}
# 	)

# 	unit_categories = {}

# 	for unit in units:
# 		unit_categories[unit.name] = unit.category

# 	booking_map = {}

# 	for booking in bookings:
# 		booking_map[booking.name] = booking

# 	for item in items:
# 		category = unit_categories.get(item.equipment_unit)

# 		if not category:
# 			continue

# 		if category not in category_data:
# 			continue

# 		booking = booking_map.get(item.parent)

# 		if not booking:
# 			continue

# 		booking_start = max(getdate(booking.start_date), from_date)
# 		booking_end = min(getdate(booking.end_date), to_date)

# 		if booking_start > booking_end:
# 			continue

# 		days = date_diff(booking_end, booking_start) + 1

# 		line_days = item.line_days or 0
# 		line_amount = item.line_amount or 0
# 		damage_fee = item.damage_fee or 0

# 		if line_days:
# 			daily_rate = line_amount / line_days
# 			rental_revenue = daily_rate * days
# 		else:
# 			rental_revenue = 0

# 		category_data[category]["days_rented"] += days
# 		category_data[category]["revenue"] += rental_revenue

# 		if damage_fee > 0:
# 			category_data[category]["damage_incidents"] += 1

# 	return build_data(category_data, from_date, to_date)


# def build_data(category_data, from_date=None, to_date=None):
# 	data = []

# 	if from_date and to_date:
# 		period_days = date_diff(to_date, from_date) + 1
# 	else:
# 		period_days = 1

# 	for category, values in category_data.items():
# 		total_units = values["total_units"]
# 		days_rented = values["days_rented"]

# 		available_days = total_units * period_days

# 		if available_days:
# 			utilization = (days_rented / available_days) * 100
# 		else:
# 			utilization = 0

# 		data.append({
# 			"category": category,
# 			"total_units": total_units,
# 			"days_rented": days_rented,
# 			"utilization": utilization,
# 			"revenue": values["revenue"],
# 			"damage_incidents": values["damage_incidents"]
# 		})

# 	return data


# def get_chart(data):
# 	return {
# 		"data": {
# 			"labels": [row["category"] for row in data],
# 			"datasets": [
# 				{
# 					"name": "Revenue",
# 					"values": [row["revenue"] for row in data]
# 				},
# 				{
# 					"name": "Damage Incidents",
# 					"values": [row["damage_incidents"] for row in data]
# 				}
# 			]
# 		},
# 		"type": "bar",
# 		"barOptions": {
# 			"stacked": False
# 		}
# 	}


# def get_report_summary(data):
# 	total_revenue = sum(row["revenue"] for row in data)
# 	total_damage = sum(row["damage_incidents"] for row in data)

# 	most_utilized = "-"

# 	if data:
# 		most_utilized = max(data, key=lambda row: row["utilization"])["category"]

# 	return [
# 		{"label": "Total Revenue", "value": total_revenue, "indicator": "Green", "datatype": "Currency"},
# 		{"label": "Total Damage Incidents", "value": total_damage, "indicator": "Red", "datatype": "Int"},
# 		{"label": "Most Utilized Category", "value": most_utilized, "indicator": "Blue", "datatype": "Data"}
# 	]