"use client";

import { useAuth } from "@/src/context/AuthContext";

export default function AdminHeader() {

  const { user } = useAuth();

  return (

    <header className="admin-header">

      <div>
        <h2>
          Welcome,
          {user?.name}
        </h2>
      </div>

      <div className="admin-user">
        {user?.email}
      </div>

    </header>

  );
}