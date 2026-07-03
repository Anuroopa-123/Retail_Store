"use client";

import { useAuth } from "@/src/context/AuthContext";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { FaUserCircle, FaSignOutAlt, FaChevronDown } from "react-icons/fa";
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
    className="user-info"
    onClick={() => setOpen(!open)}
  >
    <span>{user?.email}</span>

    <FaChevronDown
      className={`arrow ${open ? "rotate" : ""}`}
    />
  </div>

  {open && (

    <div className="profile-dropdown">

      <button
        type="button"
        onClick={() =>
          router.push("/admin/admin-profile")
        }
      >
        <FaUserCircle className="dropdown-icon" />
        My Profile
      </button>

      <button
        type="button"
        className="logout-btn"
        onClick={logout}
      >
        <FaSignOutAlt className="dropdown-icon" />
        Logout
      </button>

    </div>

  )}

</div>

    </header>

  );
}