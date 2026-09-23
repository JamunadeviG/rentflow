// Copyright (c) 2026, JamunadeviG and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Booking Item", {
//     equipment_unit(frm, cdt, cdn){
//         const row = locals[cdt][cdn]
//         frappe.db.get_value("Equipment Category", row.category, 'daily_rate').then((res)=>{
//             frappe.model.set_value(cdt, cdn, 'daily_rate', res.message.daily_rate)
//         })

//         check_for_duplicate(frm);
//     },
//     daily_rate(frm, cdt, cdn){
//         cal_line_amount(frm, cdt, cdn);
//     },
//     items_add(frm, cdt, cdn){
//         if(frm.doc.start_date==undefined || frm.doc.end_date==undefined){
//             frappe.throw("Before selecting equipment first fill out start and end dates..!")
//         }
//         cal_line_days(frm, cdt, cdn);
//     }
// })

// frappe.ui.form.on("Rental Booking", {
// 	refresh(frm) {
        
// 	}
// });


// function check_for_duplicate(frm){
//     let seen = {};
//     (frm.doc.items || []).forEach((row)=> {
//         if(!row.category) return;
//         else if(seen[row.category]){
//             frm.doc.items = frm.doc.items.filter(r=> r.name !== row.name)
//             frappe.msgprint(`Conflict occured, so this ${row.category} removed`)
//             frm.refresh_field('items')
//         }
//         else seen[row.category] = true;
//     })
// }

// function cal_line_days(frm, cdt, cdn){
//     const ld = new Date(frm.doc.end_date) - new Date(frm.doc.start_date)
//     frappe.model.set_value(cdt, cdn, 'line_days', ld / (1000*60*60*24))
// }

// function cal_line_amount(frm, cdt, cdn){
//     const row = locals[cdt][cdn]
//     console.log(row.line_days * row.daily_rate)
//     frappe.model.set_value(cdt, cdn, 'line_amount', row.line_days * row.daily_rate)
// }