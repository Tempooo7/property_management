import frappe


def validate(doc, method):
    lease_contract = getattr(doc, 'custom_lease_contract', None)

    if not lease_contract:
        return

    monthly_rent = frappe.db.get_value(
        "Lease Contract",
        lease_contract,
        "monthly_rent"
    )

    if not monthly_rent:
        frappe.throw(
            f"Could not find monthly rent for Lease Contract "
            f"{lease_contract}. "
            "Please make sure the lease exists and is submitted."
        )

    if doc.paid_amount < monthly_rent or doc.paid_amount > monthly_rent:
        frappe.throw(
            f"Payment amount ({doc.paid_amount}) cannot be less OR Bigger "
            f"than the monthly rent ({monthly_rent}) "
            f"for Lease Contract {lease_contract}."
        )