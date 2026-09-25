// Copyright (c) 2026, JamunadeviG and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Booking", {
	setup(frm) {
		frm.set_query("equipment_unit", "items", function(doc, cdt, cdn) {
			return {
				filters: {
					current_status: ["in", ["Available"]],
					is_active: 1
				}
			};
		});
	},

	refresh(frm) {
		if (frm.doc.status) {
			let indicator_color = "gray";

			if (frm.doc.status === "Draft") {
				indicator_color = "gray";
			} else if (frm.doc.status === "Confirmed") {
				indicator_color = "blue";
			} else if (frm.doc.status === "Checked Out") {
				indicator_color = "orange";
                frm.add_custom_button("Log Return", function() {
                    show_return_dialog(frm);
                });
				frm.add_custom_button("Transfer Handler", function() {
					transfer_handler(frm);
				});
			} else if (frm.doc.status === "Returned") {
				indicator_color = "green";
			} else if (frm.doc.status === "Invoiced") {
				indicator_color = "purple";
			} else if (frm.doc.status === "Closed") {
				indicator_color = "green";
			} else if (frm.doc.status === "Cancelled") {
				indicator_color = "red";
			}

			frm.dashboard.add_indicator(frm.doc.status, indicator_color);
		}
	},

	start_date(frm) {
		check_rental_period(frm);
	},

	end_date(frm) {
		check_rental_period(frm);
	}
});


function check_rental_period(frm) {
	if (!frm.doc.start_date || !frm.doc.end_date) {
		return;
	}

	let start_date = frappe.datetime.str_to_obj(frm.doc.start_date);
	let end_date = frappe.datetime.str_to_obj(frm.doc.end_date);
    if (days > 30) {
		frappe.msgprint("Rental period is more than 30 days. Please verify the dates.");
	}
	let days = frappe.datetime.get_day_diff(frm.doc.end_date, frm.doc.start_date) + 1;
	if (start_date > end_date) {
		return;
	}

	(frm.doc.items || []).forEach(row => {
		if (row.daily_rate) {
			let line_amount = days * row.daily_rate;
			frappe.model.set_value(row.doctype, row.name, "line_days", days);
			frappe.model.set_value(row.doctype, row.name, "line_amount", line_amount);
		}
	});
}


frappe.ui.form.on("Booking Item", {
	equipment_unit(frm, cdt, cdn) {
		let row = locals[cdt][cdn];

		if (row.daily_rate && frm.doc.start_date && frm.doc.end_date) {
			let days = frappe.datetime.get_day_diff(frm.doc.end_date, frm.doc.start_date) + 1;
			let line_amount = days * row.daily_rate;
			frappe.model.set_value(cdt, cdn, "line_days", days);
			frappe.model.set_value(cdt, cdn, "line_amount", line_amount);
		}
	}
});

function show_return_dialog(frm) {
	let fields = [];

	(frm.doc.items || []).forEach(row => {
		fields.push({
			fieldname: "condition_" + row.name,
			label: row.equipment_unit,
			fieldtype: "Select",
			options: "New\nGood\nFair\nPoor\nDamaged",
			reqd: 1
		});
	});

	fields.push({
		fieldname: "notes",
		label: "Notes",
		fieldtype: "Small Text"
	});

	let dialog = new frappe.ui.Dialog({
		title: "Log Return",
		fields: fields,
		primary_action_label: "Submit",
		primary_action(values) {
			let grades = {"New": 5, "Good": 4, "Fair": 3, "Poor": 2, "Damaged": 1};
			let has_drop = false;
			(frm.doc.items || []).forEach(row => {
				let checkout_grade = row.checkout_condition_grade;
				let checkin_grade = values["condition_" + row.name];
				if (checkout_grade && checkin_grade && grades[checkin_grade] < grades[checkout_grade]) {
					has_drop = true;
				}
			});

			if (has_drop && !values.notes) {
				frappe.msgprint("Notes are mandatory when the condition grade drops.");
				return;
			}

			(frm.doc.items || []).forEach(row => {
				let checkin_grade = values["condition_" + row.name];
				frappe.model.set_value(row.doctype, row.name, "checkin_condition_grade", checkin_grade);
			});

			dialog.hide();
			frm.trigger("start_date");
			frm.refresh();
		}
	});

	dialog.show();
}

function transfer_handler(frm) {
	frappe.prompt([
		{
			fieldname: "new_handler",
			label: "New Handler",
			fieldtype: "Link",
			options: "Yard Staff",
			reqd: 1
		}
	], function(values) {
		frappe.confirm("Are you sure you want to transfer this booking to " + values.new_handler + "?", function() {
			frappe.call({
				method: "rentflow.api.transfer_handler",
				args: {
					booking_name: frm.doc.name,
					new_handler: values.new_handler
				},
				callback(r) {
					if (!r.exc) {
						frappe.msgprint("Handler transferred successfully.");
						frm.reload_doc();
					}
				}
			});
		});
	}, "Transfer Handler", "Continue");
}