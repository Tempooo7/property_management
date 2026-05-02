// Copyright (c) 2026, Tamer Mohammed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Request', {

    onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value('request_date', frappe.datetime.get_today());
        }
    },

    unit: function(frm) {
        if (!frm.doc.unit) return;

        frappe.db.get_value(
            'Lease Contract',
            { unit: frm.doc.unit, docstatus: 1 },
            'tenant'
        ).then(r => {
            if (r.message && r.message.tenant) {
                frm.set_value('tenant', r.message.tenant);
            }
        });
    }
});