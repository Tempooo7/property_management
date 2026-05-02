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

                let company = frappe.defaults.get_default('company');

                if (!company) {
                    frappe.msgprint({
                        title: 'Error',
                        message: 'No default company found.',
                        indicator: 'red'
                    });
                    return;
                }

                frappe.db.get_value(
                    'Company',
                    company,
                    ['default_receivable_account', 'default_cash_account', 'default_currency']
                ).then(r => {

                    if (!r.message) {
                        frappe.msgprint({
                            title: 'Error',
                            message: 'Could not fetch company accounts.',
                            indicator: 'red'
                        });
                        return;
                    }

                    let paid_from = r.message.default_receivable_account;
                    let paid_to   = r.message.default_cash_account;
                    let currency  = r.message.default_currency || 'LYD';

                    if (!paid_from || !paid_to) {
                        frappe.msgprint({
                            title: 'Missing Account Settings',
                            message: `Please set Default Receivable Account and
                                Default Cash Account in your Company Settings.`,
                            indicator: 'orange'
                        });
                        return;
                    }

                    // Step 1 — create the Payment Entry
                    frappe.call({
                        method: 'frappe.client.insert',
                        args: {
                            doc: {
                                doctype: 'Payment Entry',
                                payment_type: 'Receive',
                                party_type: 'Customer',
                                party: frm.doc.tenant,
                                company: company,
                                posting_date: frappe.datetime.get_today(),
                                paid_from: paid_from,
                                paid_to: paid_to,
                                paid_from_account_currency: currency,
                                paid_to_account_currency: currency,
                                paid_amount: frm.doc.monthly_rent,
                                received_amount: frm.doc.monthly_rent,
                                source_exchange_rate: 1,
                                target_exchange_rate: 1,
                                remarks: `Rent payment for Lease Contract ${frm.doc.name}`
                            }
                        },
                        freeze: true,
                        freeze_message: 'Creating Payment Entry...',
                        callback: function(r) {
                            if (r.message) {
                                let pe_name = r.message.name;

                                // Step 2 — now set the custom_lease_contract
                                // field separately after the record is created.
                                // This bypasses ERPNext's before_insert logic
                                // that strips custom fields during creation.
                                frappe.call({
                                    method: 'frappe.client.set_value',
                                    args: {
                                        doctype: 'Payment Entry',
                                        name: pe_name,
                                        fieldname: 'custom_lease_contract',
                                        value: frm.doc.name
                                    },
                                    callback: function() {
                                        // Step 3 — navigate to the Payment Entry
                                        frappe.set_route(
                                            'Form',
                                            'Payment Entry',
                                            pe_name
                                        );
                                    }
                                });
                            }
                        },
                        error: function(r) {
                            frappe.msgprint({
                                title: 'Failed to Create Payment Entry',
                                message: r.message || 'Check F12 Console for details.',
                                indicator: 'red'
                            });
                        }
                    });
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

    start_date: function(frm) {
        if (frm.doc.start_date && !frm.doc.end_date) {
            let end = frappe.datetime.add_months(frm.doc.start_date, 12);
            frm.set_value('end_date', end);
        }
    },

    tenant: function(frm) {
        frm.refresh_fields();
    }

});