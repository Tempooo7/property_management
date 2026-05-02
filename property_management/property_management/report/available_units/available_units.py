# Copyright (c) 2026, Tamer Mohammed and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Unit Number", "fieldname": "unit_number", "fieldtype": "Data", "width": 150},
        {"label": "Property", "fieldname": "property", "fieldtype": "Data", "width": 200},
        {"label": "Floor", "fieldname": "floor", "fieldtype": "Data", "width": 100},
        {"label": "Size", "fieldname": "size", "fieldtype": "Data", "width": 100},
        {"label": "Rent Amount", "fieldname": "rent_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120}
    ]

    data = frappe.db.get_list(
        "Property Unit",
        filters={"status": ("in", ["Available", "Vacant", "Unoccupied"])},
        fields=["unit_number", "property", "floor", "size", "rent_amount", "status"],
        limit_page_length=500
    )

    return columns, data