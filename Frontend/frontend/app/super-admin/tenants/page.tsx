"use client";

import { useState } from "react";
import Layout from "@/app/components/layout/Layout";

export default function TenantPage() {

  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");

  const createTenant = async () => {

    await fetch(
      "http://127.0.0.1:8000/api/v1/tenants",
      {
        method: "POST",
        headers: {
          Authorization:
            `Bearer ${localStorage.getItem("access_token")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          slug,
        }),
      }
    );
  };

  return (
    <Layout>

      <h1>Create Tenant</h1>

      <input
        placeholder="Tenant Name"
        value={name}
        onChange={(e)=>
          setName(e.target.value)
        }
      />

      <input
        placeholder="Tenant Slug"
        value={slug}
        onChange={(e)=>
          setSlug(e.target.value)
        }
      />

      <button onClick={createTenant}>
        Create Tenant
      </button>

    </Layout>
  );
}