"use client";

import { useEffect, useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./superadmindashboard.css";

import {
  FaBuilding,
  FaStore,
  FaUsers,
  FaKey,
  FaUser,
  FaInbox
} from "react-icons/fa";

import {
  MdLightbulb,
  MdTrendingUp,
  MdWarning
} from "react-icons/md";

interface DashStats {
  tenants: number;
  stores: number;
  admins: number;
  roles: number;
}

interface Admin {
  id: number;
  name: string;
  status?: string;
}
interface AIInsight {
  type: "tip" | "alert" | "forecast";
  message: string;
  action?: string;
}

const aiInsights: AIInsight[] = [
  { type: "forecast", message: "Revenue trend suggests a 12% uplift this quarter if 3 pending stores go live before month-end.", action: "View stores" },
  { type: "alert",    message: "2 tenant accounts have had no activity in 30+ days — consider a re-engagement campaign.", action: "See tenants" },
  { type: "tip",      message: "Assigning role-level granularity can reduce permission conflicts by ~40%.", action: "Manage roles" },
];

export default function DashboardPage() {
  const [stats, setStats] = useState<DashStats>({ tenants: 0, stores: 0, admins: 0, roles: 0 });
  const [aiIdx, setAiIdx] = useState(0);
  const [aiLoading, setAiLoading] = useState(false);
const [recentAdmins, setRecentAdmins] =
  useState<Admin[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const [t, s, r,a] = await Promise.all([
          fetch("http://127.0.0.1:8000/api/v1/tenants").then(r => r.json()),
          fetch("http://127.0.0.1:8000/api/v1/stores").then(r => r.json()),
          fetch("http://127.0.0.1:8000/api/v1/roles/").then(r => r.json()),
          fetch("http://127.0.0.1:8000/api/v1/admins/").then(r => r.json()),
        ]);
        
        setStats({
          tenants: Array.isArray(t) ? t.length : 0,
          stores:  Array.isArray(s) ? s.length : 0,
          admins: Array.isArray(a) ? a.length : 0,
          roles:   Array.isArray(r) ? r.length : 0,
        });
        setRecentAdmins(
          Array.isArray(a)
    ? a.slice(-5).reverse()
    : []
);
      } catch { /* offline/demo */ }
    };
    load();
  }, []);

  const nextInsight = () => {
    setAiLoading(true);
    setTimeout(() => {
      setAiIdx((i) => (i + 1) % aiInsights.length);
      setAiLoading(false);
    }, 600);
  };

  const insight = aiInsights[aiIdx];
  const insightIcon = insight.type === "forecast" ? <MdTrendingUp /> : insight.type === "alert" ? <MdWarning /> : <MdLightbulb />;
  const insightColor = insight.type === "forecast" ? "var(--green)" : insight.type === "alert" ? "var(--amber)" : "var(--violet-light)";

  return (
    <Layout title="Dashboard">
      {/* Page header */}
      <div className="page-header">
        <div className="page-header-left">
          <h1>Good morning, Admin</h1>
          <p>Here what happening across your retail network today.</p>
        </div>
        <span className="dash-date">
          {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
        </span>
      </div>

      {/* Stats */}
      <div className="stats-row">
        <div className="stat-tile">
  <FaBuilding className="stat-icon" />
          <span className="tile-value">{stats.tenants}</span>
          <span className="tile-label">Active Tenants</span>
          <span className="tile-change up">↑ 2 this month</span>
        </div>
       <div className="stat-tile">
  <FaStore className="stat-icon" />
          <span className="tile-value">{stats.stores}</span>
          <span className="tile-label">Total Stores</span>
          <span className="tile-change up">↑ 5 this month</span>
        </div>
        <div className="stat-tile">
  <FaUsers className="stat-icon" />
          <span className="tile-value">{stats.admins}</span>
          <span className="tile-label">Tenant Admins</span>
          <span className="tile-change up">↑ 1 this week</span>
        </div>
       <div className="stat-tile">
  <FaKey className="stat-icon" />
          <span className="tile-value">{stats.roles}</span>
          <span className="tile-label">Roles Defined</span>
          <span className="tile-change up">Stable</span>
        </div>
      </div>

      {/* AI Planning Panel */}
      <div className="ai-panel">
        <div className="ai-panel-header">
          <div className="ai-badge">
            <span className="ai-dot" />
            AI Planning Assistant
          </div>
          <button className="ai-refresh-btn" onClick={nextInsight} disabled={aiLoading}>
            {aiLoading ? "Thinking…" : "Next insight ↻"}
          </button>
        </div>

        <div className={`ai-insight ${aiLoading ? "ai-loading" : ""}`}>
          <span className="ai-insight-icon">{insightIcon}</span>
          <div className="ai-insight-body">
            <span className="ai-insight-type" style={{ color: insightColor }}>
              {insight.type.toUpperCase()}
            </span>
            <p className="ai-insight-msg">{insight.message}</p>
          </div>
          {insight.action && (
            <button className="ai-action-btn">{insight.action} →</button>
          )}
        </div>

        <div className="ai-chips">
          <button className="ai-chip">📊 Forecast next quarter</button>
          <button className="ai-chip">🏪 Suggest new store locations</button>
          <button className="ai-chip">⚡ Optimize role assignments</button>
          <button className="ai-chip">📧 Draft tenant update email</button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="activity-section">
        <h3 className="section-title">Recent Activity</h3>
        <div className="activity-list">
      {recentAdmins.length > 0 ? (
  recentAdmins.map((admin: any) => (
    <div
      key={admin.id}
      className="activity-item"
    >
     <div className="activity-icon">
  <FaUser />
</div>

      <div className="activity-text">
        Admin {admin.name} created
      </div>

      <div className="activity-time">
        {admin.status || "Active"}
      </div>
    </div>
  ))
) : (
  <div className="activity-item">
    <div className="activity-icon">
  <FaInbox />
</div>

    <div className="activity-text">
      No recent admin activity
    </div>

    <div className="activity-time">
      --
    </div>
  </div>
)}
        </div>
      </div>
    </Layout>
  );
}