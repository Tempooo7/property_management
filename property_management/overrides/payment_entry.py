import frappe


def validate(doc, method):


    if doc.payment_type != "Receive" or doc.party_type != "Customer":
        return

    lease = frappe.db.get_value(
        "Lease Contract",
        {
            "tenant": doc.party,
            "docstatus": 1
        },
        ["name", "monthly_rent"],
        as_dict=True
    )

    if not lease:
        return

    monthly_rent = lease.monthly_rent

    if doc.paid_amount < monthly_rent:
        frappe.throw(
            f"Payment amount ({doc.paid_amount}) is less than "
            f"the monthly rent ({monthly_rent})."
        )

    if doc.paid_amount > monthly_rent:
        frappe.throw(
            f"Payment amount ({doc.paid_amount}) is greater than "
            f"the monthly rent ({monthly_rent})."
        )