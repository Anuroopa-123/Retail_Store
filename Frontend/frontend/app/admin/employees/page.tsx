"use client";

import "./employees.css";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";

export default function EmployeesPage() {

  return (

    <AdminLayout>

      <div className="employee-container">

        <div className="employee-header">

          <h1 className="employee-title">
            Employee Management
          </h1>

          <button className="add-btn">
            + Add Employee
          </button>

        </div>

        <input
          className="search-box"
          placeholder="Search Employee..."
        />

        <div className="table-container">

          <table>

            <thead>

              <tr>
                <th>ID</th>
                <th>Employee Code</th>
                <th>Name</th>
                <th>Department</th>
                <th>Status</th>
              </tr>

            </thead>

            <tbody>

              <tr>
                <td>1</td>
                <td>EMP001</td>
                <td>Rahul</td>
                <td>Sales</td>
                <td>
                  <span className="status-badge">
                    Active
                  </span>
                </td>
              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </AdminLayout>

  );
}