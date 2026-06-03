"use client";

import { useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./tenants.css";

export default function TenantPage() {

  const [name, setName] = useState("");
//   const [slug, setSlug] = useState("");

  const createTenant = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/tenants",
        {
          method: "POST",
          headers: {
            Authorization:
              `Bearer ${localStorage.getItem(
                "access_token"
              )}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail);
        return;
      }

      alert("Tenant Created Successfully");

      setName("");
    //   setSlug("");

    } catch (error) {
      console.error(error);
      alert("Something went wrong");
    }
  };

  return (
    <Layout>

      <div className="tenant-page">

        <h1>Create Tenant</h1>

        <div className="form-group">
          <input
            placeholder="Tenant Name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
          />
        </div>

        {/* <div className="form-group">
          <input
            placeholder="Tenant Slug"
            value={slug}
            onChange={(e) =>
              setSlug(e.target.value)
            }
          />
        </div> */}

        <button
          className="create-btn"
          onClick={createTenant}
        >
          Create Tenant
        </button>

      </div>

    </Layout>
  );
}