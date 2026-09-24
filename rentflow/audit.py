import frappe


def log_change(doc, method):
	if doc.doctype == "Audit Log":
		return

	audit_log = frappe.get_doc({
		"doctype": "Audit Log",
		"doctype_name": doc.doctype,
		"document_name": doc.name,
		"action": method,
		"user": frappe.session.user,
		"timestamp": frappe.utils.now()
	})

	audit_log.insert(ignore_permissions=True)