"use client";

import { useEffect, useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./dashboard.css";

interface DashStats {
  tenants: number;
  stores: number;
  admins: number;
  roles: number;
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

  useEffect(() => {
    const load = async () => {
      try {
        const [t, s, r] = await Promise.all([
          fetch("http://127.0.0.1:8000/api/v1/tenants").then(r => r.json()),
          fetch("http://127.0.0.1:8000/api/v1/stores").then(r => r.json()),
          fetch("http://127.0.0.1:8000/api/v1/roles/").then(r => r.json()),
        ]);
        setStats({
          tenants: Array.isArray(t) ? t.length : 0,
          stores:  Array.isArray(s) ? s.length : 0,
          admins:  0,
          roles:   Array.isArray(r) ? r.length : 0,
        });
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
  const insightIcon = insight.type === "forecast" ? "📈" : insight.type === "alert" ? "⚠️" : "💡";
  const insightColor = insight.type === "forecast" ? "var(--green)" : insight.type === "alert" ? "var(--amber)" : "var(--violet-light)";

  return (
    <Layout title="Dashboard">
      {/* Page header */}
      <div className="page-header">
        <div className="page-header-left">
          <h1>Good morning, Admin 👋</h1>
          <p>Here's what's happening across your retail network today.</p>
        </div>
        <span className="dash-date">
          {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
        </span>
      </div>

      {/* Stats */}
      <div className="stats-row">
        <div className="stat-tile" data-icon="🏢">
          <span className="tile-value">{stats.tenants}</span>
          <span className="tile-label">Active Tenants</span>
          <span className="tile-change up">↑ 2 this month</span>
        </div>
        <div className="stat-tile" data-icon="🏪">
          <span className="tile-value">{stats.stores}</span>
          <span className="tile-label">Total Stores</span>
          <span className="tile-change up">↑ 5 this month</span>
        </div>
        <div className="stat-tile" data-icon="👥">
          <span className="tile-value">{stats.admins}</span>
          <span className="tile-label">Tenant Admins</span>
          <span className="tile-change up">↑ 1 this week</span>
        </div>
        <div className="stat-tile" data-icon="🔑">
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
          {[
            { icon: "🏢", text: "New tenant \"Metro Mart\" onboarded", time: "2h ago", type: "create" },
            { icon: "🏪", text: "Store #42 \"Downtown Branch\" went live", time: "5h ago", type: "create" },
            { icon: "🔑", text: "Role \"Store Manager\" permissions updated", time: "1d ago", type: "update" },
            { icon: "👤", text: "Admin Priya S. added to tenant TechMall", time: "1d ago", type: "create" },
          ].map((item, i) => (
            <div key={i} className="activity-item">
              <div className="activity-icon">{item.icon}</div>
              <div className="activity-text">{item.text}</div>
              <div className="activity-time">{item.time}</div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}