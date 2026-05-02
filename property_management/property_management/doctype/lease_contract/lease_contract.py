# Copyright (c) 2026, Tamer Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class LeaseContract(Document):

    def validate(self):
        self.validate_dates()
        self.check_unit_availability()
        self.fetch_unit_rent()

    def on_submit(self):
        self.db_set("status", "Active")
        self.refresh_unit_status()

        frappe.msgprint(
            f"Lease Contract submitted. Unit {self.unit} Property now is occupied.",
            indicator="green"
        )

    def on_cancel(self):
        self.db_set("status", "Cancelled")
        self.refresh_unit_status()

        frappe.msgprint(
            f"Lease cancelled. Unit {self.unit} Property is now available.",
            indicator="blue"
        )

    

    def validate_dates(self):
        if not self.start_date or not self.end_date:
            return

        if getdate(self.end_date) <= getdate(self.start_date):
            frappe.throw(
                f"End Date must be after Start Date. "
                f"You entered Start Date: {self.start_date}, End Date: {self.end_date}."
            )

    def check_unit_availability(self):
        if not self.unit:
            return

        status = frappe.db.get_value("Property Unit", self.unit, "status")
        if status == "Occupied":
            frappe.throw(
                f"Unit {self.unit} is already Occupied. Please select another unit."
            )

        if status == "Maintenance":
            frappe.throw(
                f"Unit {self.unit} is under Maintenance. Please select another unit."
            )


    def refresh_unit_status(self):
        today = getdate(nowdate())

        active = frappe.db.exists("Lease Contract", {
            "unit": self.unit,
            "status": "Active",
            "start_date": ["<=", today],
            "end_date": [">=", today]
        })

        status = "Occupied" if active else "Available"

        frappe.db.set_value("Property Unit", self.unit, "status", status)



    def fetch_unit_rent(self):
        if self.unit and not self.monthly_rent:
            rent = frappe.db.get_value("Property Unit", self.unit, "rent_amount")
            if rent:
                self.monthly_rent = rent