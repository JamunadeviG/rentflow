// frappe.query_reports["Equipment Utilization"] = {
// 	filters: [
// 		{
// 			fieldname: "from_date",
// 			label: "From Date",
// 			fieldtype: "Date",
// 			default: frappe.datetime.add_days(frappe.datetime.get_today(), -30),
// 			reqd: 1
// 		},
// 		{
// 			fieldname: "to_date",
// 			label: "To Date",
// 			fieldtype: "Date",
// 			default: frappe.datetime.get_today(),
// 			reqd: 1
// 		},
// 		{
// 			fieldname: "category",
// 			label: "Category",
// 			fieldtype: "Link",
// 			options: "Equipment Category"
// 		}
// 	],

// 	formatter: function(value, row, column, data) {
// 		if (column.fieldname === "utilization") {
// 			let percentage = parseFloat(value) || 0;

// 			if (percentage < 30) {
// 				return `<span style="color:red">${percentage.toFixed(2)}%</span>`;
// 			}

// 			if (percentage >= 70) {
// 				return `<span style="color:green">${percentage.toFixed(2)}%</span>`;
// 			}

// 			return `${percentage.toFixed(2)}%`;
// 		}

// 		if (column.fieldname === "category") {
// 			return `<a href="/app/equipment-category/${encodeURIComponent(value)}">${value}</a>`;
// 		}

// 		return value;
// 	}
// };