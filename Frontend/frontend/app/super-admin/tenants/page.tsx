"use client";

import { useEffect, useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./tenants.css";
import toast from "react-hot-toast";
import { Tenant } from "@/src/types/tenant";

export default function TenantPage() {

  const [name, setName] = useState("");

const [tenants, setTenants] =
  useState<Tenant[]>([]);

  const [showForm, setShowForm] =
    useState(false);
    const [searchTerm, setSearchTerm] =
  useState("");

  const getTenants = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/tenants"
      );

      const data =
        await response.json();

      setTenants(data);

    } catch(error) {
      console.log(error);
    }
  };

useEffect(() => {

  const load = async () => {
    await getTenants();
  };

  load();

}, []);

  const createTenant = async () => {

    const response = await fetch(
      "http://127.0.0.1:8000/api/v1/tenants",
      {
        method:"POST",

        headers:{
          "Content-Type":
            "application/json",

          Authorization:
            `Bearer ${localStorage.getItem(
              "access_token"
            )}`
        },

        body:JSON.stringify({
          name
        })
      }
    );

    if(response.ok){
       toast.success(
    "Tenant created successfully "
  );

      setName("");

      setShowForm(false);

      getTenants();
    } else {
      toast.error(
        "Failed to create tenant"
      );
    }

    
  };
      const filteredTenants =
  tenants.filter(
    (tenant) =>
      tenant.name
        .toLowerCase()
        .includes(
          searchTerm.toLowerCase()
        ) ||

      tenant.slug
        .toLowerCase()
        .includes(
          searchTerm.toLowerCase()
        )
  );
  

  return (

    <Layout>

      <div className="page-header">

        <h1>Tenant Management</h1>

        <button
          className="add-btn"
          onClick={() =>
            setShowForm(true)
          }
        >
          + Add Tenant
        </button>

      </div>

    <input
  className="search-box"
  placeholder="Search Tenant..."
  value={searchTerm}
  onChange={(e) =>
    setSearchTerm(
      e.target.value
    )
  }
/>

      {showForm && (

        <div className="tenant-card">

          <h2>Create Tenant</h2>

          <input
            placeholder="Tenant Name"
            value={name}
            onChange={(e)=>
              setName(
                e.target.value
              )
            }
          />

          <button
            className="save-btn"
            onClick={createTenant}
          >
            Save
          </button>

        </div>

      )}

      <div className="table-container">

        <table>

          <thead>

            <tr>

              <th>S.No</th>
              <th>Name</th>
              <th>Slug</th>
              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            {filteredTenants.map(
              (tenant,index)=>(
                <tr
                  key={tenant.id}
                >
                  <td>
                    {index + 1}
                  </td>

                  <td>
                    {tenant.name}
                  </td>

                  <td>
                    {tenant.slug}
                  </td>

              <td>

  <span
    className={`status-badge ${tenant.status}`}
  >
    {tenant.status}
  </span>

</td>
                </tr>
              )
            )}

          </tbody>

        </table>

      </div>

    </Layout>
  );
}
