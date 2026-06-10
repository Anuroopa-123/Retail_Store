"use client";

import Sidebar from "./sidebar";
import "./sidebar.css";

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
}

export default function Layout({ children, title = "RetailIQ" }: LayoutProps) {
  return (
    <div className="layout-wrapper">
      <Sidebar />
      <div className="main-content">
        <header className="topbar">
          <span className="topbar-title">{title}</span>
          <div className="topbar-right">
            <div className="topbar-notif">🔔</div>
            <div className="topbar-avatar">SA</div>
          </div>
        </header>
        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
}