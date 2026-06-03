import Layout from "@/app/components/layout/Layout";
import "./dashboard.css";

export default function DashboardPage() {
  return (
    <Layout>

      <div className="dashboard-container">

        <div className="dashboard-header">
          <h1>Welcome Super Admin</h1>
          <p>
            Manage Tenants, Stores and Admins
          </p>
        </div>

        <div className="stats-grid">

          <div className="stat-card">
            <h3>Total Tenants</h3>
            <div className="stat-number">
              10
            </div>
          </div>

          <div className="stat-card">
            <h3>Total Stores</h3>
            <div className="stat-number">
              25
            </div>
          </div>

          <div className="stat-card">
            <h3>Total Admins</h3>
            <div className="stat-number">
              8
            </div>
          </div>

        </div>

      </div>

    </Layout>
  );
}