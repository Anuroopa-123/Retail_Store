"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <div className="sidebar">

      <h2>Retail Store</h2>

      <ul>

        <li>
          <Link href="/super-admin/dashboard">
            Dashboard
          </Link>
        </li>

        <li>
          <Link href="/super-admin/tenants">
            Tenants
          </Link>
        </li>

        <li>
          <Link href="/super-admin/stores">
            Stores
          </Link>
        </li>

        <li>
          <Link href="/super-admin/admins">
            Tenant Admins
          </Link>
        </li>

        <li>
          <Link href="/super-admin/roles">
            Roles
          </Link>
        </li>

      </ul>

    </div>
  );
}