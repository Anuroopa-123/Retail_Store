"use client";

import { useEffect, useState } from "react";
import Layout from "@/app/components/layout/Layout";
import "./stores.css";
import { Tenant } from "@/src/types/tenant";

export default function StorePage() {
    
const [tenants,setTenants] =
  useState<Tenant[]>([]);

  const [tenantId,setTenantId] =
    useState("");

  const [name,setName] =
    useState("");

  const [email,setEmail] =
    useState("");

  const [phone,setPhone] =
    useState("");

  useEffect(()=>{

    fetch(
      "http://127.0.0.1:8000/api/v1/tenants"
    )
    .then(res=>res.json())
    .then(data=>setTenants(data));

  },[]);

  const createStore = async()=>{

    await fetch(
      "http://127.0.0.1:8000/api/v1/stores",
      {
        method:"POST",

        headers:{
          "Content-Type":
            "application/json"
        },

        body:JSON.stringify({

          tenant_id:
            Number(tenantId),

          name,
          email,
          phone

        })
      }
    );
  };

  return(

    <Layout>

      <div className="store-card">

        <h1>Create Store</h1>

        <select
          value={tenantId}
          onChange={(e)=>
            setTenantId(
              e.target.value
            )
          }
        >

          <option value="">
            Select Tenant
          </option>

          {tenants.map(
            (tenant)=>(
              <option
                key={tenant.id}
                value={tenant.id}
              >
                {tenant.name}
              </option>
            )
          )}

        </select>

        <input
          placeholder="Store Name"
          value={name}
          onChange={(e)=>
            setName(
              e.target.value
            )
          }
        />

        <input
          placeholder="Store Email"
          value={email}
          onChange={(e)=>
            setEmail(
              e.target.value
            )
          }
        />

        <input
          placeholder="Store Phone"
          value={phone}
          onChange={(e)=>
            setPhone(
              e.target.value
            )
          }
        />

        <button
          onClick={createStore}
        >
          Create Store
        </button>

      </div>

    </Layout>
  );
}