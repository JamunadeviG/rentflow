// Copyright (c) 2026, JamunadeviG and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Invoice", {
	refresh(frm) {
        frm.set_value("invoice_date", frappe.datetime.get_today())
	},
});
