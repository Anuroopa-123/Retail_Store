"use client";

import {
  useEffect,
  useState,
} from "react";

export default function Dashboard() {

  const [user, setUser] =
    useState<any>(null);

  useEffect(() => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/me`,
      {
        headers: {
          Authorization:
            `Bearer ${token}`,
        },
      }
    )
      .then((r) => r.json())
      .then(setUser);

  }, []);

  if (!user)
    return <p>Loading...</p>;

  return (
    <div
      style={{
        padding: "40px",
      }}
    >
      <h1>
        Welcome {user.name}
      </h1>

      <p>
        Email:
        {user.email}
      </p>

      <p>
        Status:
        {user.status}
      </p>

      <p>
        Tenant:
        {user.tenant_id}
      </p>

      <p>
        Store:
        {user.store_id}
      </p>

      <p>
        Roles:
        {user.roles?.join(", ")}
      </p>
    </div>
  );
}