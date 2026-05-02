# Copyright (c) 2026, Tamer Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class MaintenanceRequest(Document):

    def validate(self):
        if not self.request_date:
            self.request_date = nowdate()

        self.validate_tenant_unit_match()

    def on_submit(self):
        frappe.db.set_value("Property Unit", self.unit, "status", "Maintenance")

        frappe.msgprint(
            f"Unit <b>{self.unit}</b> has been set to Maintenance",
            indicator="orange",
            title="Unit Status Updated"
        )

    def on_cancel(self):
        frappe.db.set_value("Property Unit", self.unit, "status", "Available")

        frappe.msgprint(
            f"Unit <b>{self.unit}</b> has been set to Available",
            indicator="green",
            title="Unit Status Updated"
        )

    def validate_tenant_unit_match(self):
        if not self.unit or not self.tenant:
            return

        lease_exists = frappe.db.exists("Lease Contract", {
            "unit": self.unit,
            "tenant": self.tenant,
            "docstatus": 1
        })

        if not lease_exists:
            frappe.throw(
                f"Tenant <b>{self.tenant}</b> does not have an active "
                f"lease on unit <b>{self.unit}</b>. "
                "Please select the correct unit or tenant."
            )