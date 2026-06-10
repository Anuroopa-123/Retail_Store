"use client";

import { useEffect, useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./admins.css";
import toast from "react-hot-toast";

interface Tenant {
  id: number;
  name: string;
}

interface Store {
  id: number;
  name: string;
}

interface Admin {
  id: number;
  name: string;
  email: string;
  status: string;
}

export default function AdminPage() {

  const [tenants, setTenants] =
    useState<Tenant[]>([]);

  const [stores, setStores] =
    useState<Store[]>([]);

  const [admins, setAdmins] =
    useState<Admin[]>([]);

  const [tenantId, setTenantId] =
    useState("");

  const [storeId, setStoreId] =
    useState("");

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const loadAdmins = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/admins/"
      );

      const data =
        await response.json();

      setAdmins(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (error) {

      console.error(error);

      setAdmins([]);
    }
  };

  useEffect(() => {

    const loadData = async () => {

      try {

        const tenantResponse =
          await fetch(
            "http://127.0.0.1:8000/api/v1/tenants/"
          );

        const tenantData =
          await tenantResponse.json();

        setTenants(
          Array.isArray(tenantData)
            ? tenantData
            : []
        );

        const storeResponse =
          await fetch(
            "http://127.0.0.1:8000/api/v1/stores/"
          );

        const storeData =
          await storeResponse.json();

        setStores(
          Array.isArray(storeData)
            ? storeData
            : []
        );

        await loadAdmins();

      } catch (error) {

        console.error(error);
      }
    };

    loadData();

  }, []);

  const createAdmin = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/admins/",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            tenant_id:
              Number(tenantId),

            store_id:
              Number(storeId),

            name,
            email,
            password,
          }),
        }
      );

      if (!response.ok) {

        const error =
          await response.json();

        toast.error(
  error.detail ||
  "Failed to create admin"
);

        return;
      }

   toast.success(
  "Admin created successfully "
);

      setTenantId("");
      setStoreId("");
      setName("");
      setEmail("");
      setPassword("");

      await loadAdmins();

    } catch (error) {

      console.error(error);

      toast.error(
  "Something went wrong"
);
    }
  };

  return (

    <Layout>

      <div className="page-container">

        <h1 className="page-title">
          Tenant Admin Management
        </h1>

        <div className="admin-card">

          <select
            value={tenantId}
            onChange={(e) =>
              setTenantId(
                e.target.value
              )
            }
          >

            <option value="">
              Select Tenant
            </option>

            {tenants.map(
              (tenant) => (

                <option
                  key={tenant.id}
                  value={tenant.id}
                >
                  {tenant.name}
                </option>

              )
            )}

          </select>

          <select
            value={storeId}
            onChange={(e) =>
              setStoreId(
                e.target.value
              )
            }
          >

            <option value="">
              Select Store
            </option>

            {stores.map(
              (store) => (

                <option
                  key={store.id}
                  value={store.id}
                >
                  {store.name}
                </option>

              )
            )}

          </select>

          <input
            placeholder="Admin Name"
            value={name}
            onChange={(e) =>
              setName(
                e.target.value
              )
            }
          />

          <input
            placeholder="Admin Email"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          <button
            className="create-admin-btn"
            onClick={createAdmin}
          >
            Create Admin
          </button>

        </div>

        <table className="admin-table">

          <thead>

            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
            </tr>

          </thead>

          <tbody>

            {admins.map(
              (admin) => (

                <tr
                  key={admin.id}
                >

                  <td>
                    {admin.name}
                  </td>

                  <td>
                    {admin.email}
                  </td>

                <td>

  <span
    className={`status-badge ${admin.status}`}
  >
    {admin.status}
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