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
                frappe.new_doc('Payment', {
                    lease_contract: frm.doc.name,
                    tenant: frm.doc.tenant,
                    amount: frm.doc.monthly_rent
                });
            }, 'Actions');
        }
    },

    
    unit: function(frm) {
        if (!frm.doc.unit) return;

        frappe.db.get_value(
            'Property Unit',
            frm.doc.unit,
            ['rent_amount', 'property']
        ).then(r => {
            if (r.message) {
                frm.set_value('monthly_rent', r.message.rent_amount);
                frm.set_value('property', r.message.property);
            }
        });
    },

});