import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8001").rstrip("/")

st.set_page_config(page_title="Bug & Employee Manager", layout="wide")
st.title("Bug & Employee Management")
st.caption(f"API endpoint: {BASE_URL}")

tab_employees, tab_bugs = st.tabs(["Employees", "Bugs"])

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def api(method: str, path: str, **kwargs):
    try:
        resp = requests.request(method, BASE_URL + path, **kwargs)
        return resp
    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to API. Set API_BASE_URL to the bug-employee-api address and make sure the API is running."
        )
        return None

# ---------------------------------------------------------------------------
# EMPLOYEES TAB
# ---------------------------------------------------------------------------

with tab_employees:
    st.header("Employees")

    # ---- List employees ----
    if st.button("Refresh Employees"):
        st.session_state["employees_refresh"] = True

    resp = api("GET", "/employees")
    employees = resp.json() if resp and resp.ok else []

    if employees:
        st.dataframe(employees, use_container_width=True)
    else:
        st.info("No employees found.")

    st.divider()

    # ---- Create employee ----
    with st.expander("Add New Employee"):
        with st.form("create_employee_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            role = st.selectbox("Role", ["developer", "tester", "manager"])
            active = st.checkbox("Active", value=True)
            submitted = st.form_submit_button("Create")
            if submitted:
                if not name or not email:
                    st.warning("Name and Email are required.")
                else:
                    r = api("POST", "/employees", json={"name": name, "email": email, "role": role, "active": active})
                    if r and r.status_code == 201:
                        st.success(f"Employee created: {r.json()}")
                        st.rerun()
                    elif r:
                        st.error(r.json())

    # ---- Update employee ----
    with st.expander("Update Employee"):
        with st.form("update_employee_form"):
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            u_name = st.text_input("New Name (leave blank to keep)")
            u_email = st.text_input("New Email (leave blank to keep)")
            u_role = st.selectbox("New Role (leave as-is to keep)", ["", "developer", "tester", "manager"])
            u_active = st.selectbox("Active", ["", "true", "false"])
            patch_submitted = st.form_submit_button("Update (PATCH)")
            if patch_submitted:
                payload = {}
                if u_name:
                    payload["name"] = u_name
                if u_email:
                    payload["email"] = u_email
                if u_role:
                    payload["role"] = u_role
                if u_active:
                    payload["active"] = u_active == "true"
                if not payload:
                    st.warning("Provide at least one field to update.")
                else:
                    r = api("PATCH", f"/employees/{int(emp_id)}", json=payload)
                    if r and r.ok:
                        st.success(f"Updated: {r.json()}")
                        st.rerun()
                    elif r:
                        st.error(r.json())

    # ---- Delete employee ----
    with st.expander("Delete Employee"):
        with st.form("delete_employee_form"):
            del_emp_id = st.number_input("Employee ID to delete", min_value=1, step=1)
            del_submitted = st.form_submit_button("Delete")
            if del_submitted:
                r = api("DELETE", f"/employees/{int(del_emp_id)}")
                if r and r.status_code == 204:
                    st.success("Employee deleted.")
                    st.rerun()
                elif r:
                    st.error(r.json())

# ---------------------------------------------------------------------------
# BUGS TAB
# ---------------------------------------------------------------------------

with tab_bugs:
    st.header("Bugs")

    resp = api("GET", "/bugs")
    bugs = resp.json() if resp and resp.ok else []

    if bugs:
        st.dataframe(bugs, use_container_width=True)
    else:
        st.info("No bugs found.")

    st.divider()

    # ---- Create bug ----
    with st.expander("Report New Bug"):
        with st.form("create_bug_form"):
            b_title = st.text_input("Title")
            b_desc = st.text_area("Description")
            b_priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
            b_status = st.selectbox("Status", ["open", "in_progress", "resolved", "closed"])
            b_created_by = st.number_input("Created By Employee ID", min_value=1, step=1)
            b_assigned_to = st.number_input("Assigned To Employee ID (0 = none)", min_value=0, step=1)
            b_submitted = st.form_submit_button("Create Bug")
            if b_submitted:
                if not b_title or not b_desc:
                    st.warning("Title and Description are required.")
                else:
                    payload = {
                        "title": b_title,
                        "description": b_desc,
                        "priority": b_priority,
                        "status": b_status,
                        "created_by_employee_id": int(b_created_by),
                    }
                    if b_assigned_to > 0:
                        payload["assigned_to_employee_id"] = int(b_assigned_to)
                    r = api("POST", "/bugs", json=payload)
                    if r and r.status_code == 201:
                        st.success(f"Bug created: {r.json()}")
                        st.rerun()
                    elif r:
                        st.error(r.json())

    # ---- Update bug ----
    with st.expander("Update Bug"):
        with st.form("update_bug_form"):
            ub_id = st.number_input("Bug ID", min_value=1, step=1)
            ub_title = st.text_input("New Title (leave blank to keep)")
            ub_desc = st.text_area("New Description (leave blank to keep)")
            ub_priority = st.selectbox("New Priority", ["", "low", "medium", "high", "critical"])
            ub_status = st.selectbox("New Status", ["", "open", "in_progress", "resolved", "closed"])
            ub_assigned = st.number_input("Assigned To Employee ID (-1 = keep, 0 = unassign)", min_value=-1, step=1, value=-1)
            ub_submitted = st.form_submit_button("Update Bug (PATCH)")
            if ub_submitted:
                payload = {}
                if ub_title:
                    payload["title"] = ub_title
                if ub_desc:
                    payload["description"] = ub_desc
                if ub_priority:
                    payload["priority"] = ub_priority
                if ub_status:
                    payload["status"] = ub_status
                if ub_assigned == 0:
                    payload["assigned_to_employee_id"] = None
                elif ub_assigned > 0:
                    payload["assigned_to_employee_id"] = int(ub_assigned)
                if not payload:
                    st.warning("Provide at least one field to update.")
                else:
                    r = api("PATCH", f"/bugs/{int(ub_id)}", json=payload)
                    if r and r.ok:
                        st.success(f"Updated: {r.json()}")
                        st.rerun()
                    elif r:
                        st.error(r.json())

    # ---- Delete bug ----
    with st.expander("Delete Bug"):
        with st.form("delete_bug_form"):
            del_bug_id = st.number_input("Bug ID to delete", min_value=1, step=1)
            del_bug_submitted = st.form_submit_button("Delete Bug")
            if del_bug_submitted:
                r = api("DELETE", f"/bugs/{int(del_bug_id)}")
                if r and r.status_code == 204:
                    st.success("Bug deleted.")
                    st.rerun()
                elif r:
                    st.error(r.json())
