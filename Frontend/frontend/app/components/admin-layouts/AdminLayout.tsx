"use client";

import "./AdminLayout.css";
import AdminSidebar from "./AdminSidebar";
import AdminHeader from "./AdminHeader";

interface Props {
  children: React.ReactNode;
}

export default function AdminLayout({
  children,
}: Props) {

  return (

    <div className="admin-layout">

      <AdminSidebar />

      <div className="admin-main">

        <AdminHeader />

        <div className="admin-content">
          {children}
        </div>

      </div>

    </div>

  );
}