# Copyright (c) 2026, Tamer Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class LeaseContract(Document):
    
    def validate(self):
        # All these must be indented exactly 8 spaces (2 levels in)
        pass
        
        
        
        

    def on_submit(self):
        self.set_unit_status("Occupied")
        self.db_set("status", "Active")
        frappe.msgprint(
            f"Lease Contract submitted. Unit {self.unit} is now Occupied.",
            indicator="green"
        )

    def on_cancel(self):    
        self.set_unit_status("Available")
        self.db_set("status", "Cancelled")
        frappe.msgprint(
            f"Lease cancelled. Unit {self.unit} is now Available.",
            indicator="blue"
        )



    def validate_dates(self):
        if not self.start_date or not self.end_date:
            return
        if getdate(self.end_date) <= getdate(self.start_date):
            frappe.throw(
                "End Date must be after Start Date."
                 f"You enterd Start Date: {self.start_date}, End: {self.end_date}."
                 )
            
    def check_unit_availability(self):
        if not self.unit:
            return
        status = frappe.db.get_value("Property Unit", self.unit, "status")
        if status == "Occupied":
            frappe.throw(
                f"Unit {self.unit} is currently Occupied. Please select a different unit."
            )
        if status == "Maintenance":
            frappe.throw(
                f"Unit {self.unit} is currently under Maintenance. Please select a different unit."
            )
    def check_lease_overlap(self):
        if not self.unit or not self.start_date or not self.end_date:
            return
        overlapping_leases = frappe.db.sql("""
            SELECT name FROM `tabLease Contract`
            WHERE unit = %s
            AND status = 'Active'
            AND (
                (start_date <= %s AND end_date >= %s) OR
                (start_date <= %s AND end_date >= %s) OR
                (start_date >= %s AND end_date <= %s)
            )
        """, (
            self.unit,
            self.start_date, self.start_date,
            self.end_date, self.end_date,
            self.start_date, self.end_date
        ), as_dict=True)
        
        if overlapping_leases:
            lease_names = ", ".join([lease.name for lease in overlapping_leases])
            frappe.throw(
                f"Unit {self.unit} has overlapping active leases: {lease_names}. Please adjust the dates or select a different unit."
            )
    def fetch_unit_rent(self):
        if not self.unit and self.monthly_rent:
            rent = frappe.db.get_value("Property Unit", self.unit, "rent_amount")
            if rent:
                self.monthly_rent=rent


    def set_unit_status(self, status):
        """Update the linked unit's status in the database."""
        frappe.db.set_value(
            "Property Unit",
            self.unit,
            "status",
            status
        )
        frappe.db.commit()