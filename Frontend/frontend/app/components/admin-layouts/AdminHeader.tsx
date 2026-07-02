"use client";

import { useAuth } from "@/src/context/AuthContext";
import { useState } from "react";
import { useRouter } from "next/navigation";
import './AdminHeader.css';

export default function AdminHeader() {

  const { user ,logout} = useAuth();
  const router=useRouter();

const [open,setOpen]=useState(false);

  return (

    <header className="admin-header">

      <div>
        <h2>
          Welcome,
          {user?.name}
        </h2>
      </div>

     <div className="admin-user">

<div
onClick={()=>setOpen(!open)}
>

{user?.email} ▼

</div>

{open && (

<div className="profile-dropdown">

<button
onClick={()=>router.push("/admin/admin-profile")}
>

My Profile

</button>

<button
onClick={logout}
>

Logout

</button>

</div>

)}

</div>

    </header>

  );
}