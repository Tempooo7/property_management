// Copyright (c) 2026, Tamer Mohammed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lease Contract', {

    onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value('start_date', frappe.datetime.get_today());
        }
    },

    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button('Make Payment', function() {
                frappe.new_doc('Payment Entry', {
                    payment_type: 'Receive',
                    party_type: 'Customer',
                    party: frm.doc.tenant,
                    remarks: `Rent payment for Lease Contract ${frm.doc.name}`
                });
            }, 'Actions');
        }
    },

    unit: function(frm) {
        if (!frm.doc.unit) return;
        frappe.db.get_value('Property Unit', frm.doc.unit, ['rent_amount', 'property'])
            .then(r => {
                if (r.message) {
                    frm.set_value('monthly_rent', r.message.rent_amount);
                    frm.set_value('property', r.message.property);
                }
            });
    },

    start_date: function(frm) {
        if (frm.doc.start_date && !frm.doc.end_date) {
            frm.set_value('end_date', frappe.datetime.add_months(frm.doc.start_date, 12));
        }
    }

});