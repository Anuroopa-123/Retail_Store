"use client";

import { useAuth } from "@/src/context/AuthContext";

export default function AdminDashboard() {

  const { user } = useAuth();

  return (
    <div style={{ padding: "30px" }}>
      <h1>
        Admin Dashboard
      </h1>

      <h3>
        Welcome {user?.name}
      </h3>

      <p>
        Email: {user?.email}
      </p>

      <p>
        {/* Status: {user?.status} */}
      </p>
    </div>
  );
}