"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import "./sidebar.css";

const navItems = [
  { href: "/super-admin/dashboard", icon: "📊", label: "Dashboard" },
  { href: "/super-admin/tenants",   icon: "🏢", label: "Tenants" },
  { href: "/super-admin/stores",    icon: "🏪", label: "Stores" },
  { href: "/super-admin/admins",    icon: "👥", label: "Tenant Admins" },
  { href: "/super-admin/roles",     icon: "🔑", label: "Roles" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/auth/login");
  };

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-header">
        <Link href="/super-admin/dashboard" className="sidebar-logo">
          <div className="sidebar-logo-icon">🛍️</div>
          <span className="sidebar-logo-text">Retail<span>IQ</span></span>
        </Link>
      </div>

      <div className="sidebar-role">Super Admin</div>

      {/* Navigation */}
      <div className="sidebar-section-label">Management</div>
      <ul className="sidebar-nav">
        {navItems.map((item) => (
          <li key={item.href}>
            <Link
              href={item.href}
              className={pathname === item.href ? "active" : ""}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </Link>
          </li>
        ))}
      </ul>

      {/* Logout */}
      <div className="sidebar-footer">
        <button className="logout-btn" onClick={handleLogout}>
          <span className="nav-icon">🚪</span>
          Sign Out
        </button>
      </div>
    </aside>
  );
}