"use client";

import "./admindashboard.css";
import { useAuth } from "@/src/context/AuthContext";
import AdminLayout from "@/app/components/admin-layouts/AdminLayout";



export default function AdminDashboard() {

  const { user } = useAuth();

  return (

    <AdminLayout>

      <div className="dashboard-container">

        <h1 className="dashboard-title">
          Admin Dashboard
        </h1>

        <p className="dashboard-subtitle">
          Welcome {user?.name}
        </p>

        <div className="dashboard-grid">

          <div className="dashboard-card">
            <h3>Total Employees</h3>
            <h2>0</h2>
          </div>

          <div className="dashboard-card">
            <h3>Present Today</h3>
            <h2>0</h2>
          </div>

          <div className="dashboard-card">
            <h3>Pending Leaves</h3>
            <h2>0</h2>
          </div>

          <div className="dashboard-card">
            <h3>Payroll</h3>
            <h2>₹0</h2>
          </div>

        </div>

      </div>

    </AdminLayout>

  );
}