"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import "./login.css";
import { login } from "@/src/lib/api/auth";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async (e: React.FormEvent) => {
    e.preventDefault();

    const response = await fetch(
      "http://127.0.0.1:8000/api/v1/auth/login",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      }
    );

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "refresh_token",
        data.refresh_token
      );

      router.push( "/super-admin/dashboard");
    } else {
      alert(data.detail);
    }
  };

  return (
  <div className="login-container">

    <div className="left-panel">

      <form
        className="login-form"
        onSubmit={login}
      >

        <h1>Retail Store</h1>

        <div className="input-group">
          <input
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />
        </div>

        <div className="input-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />
        </div>

        <button
          className="login-btn"
          type="submit"
        >
          Login
        </button>

      </form>

    </div>

    <div className="right-panel">
      <h2>Retail Store</h2>
    </div>

  </div>
);
}