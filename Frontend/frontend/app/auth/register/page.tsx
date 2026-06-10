"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] =
    useState("");

  const register = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/register`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json",
        },
        body: JSON.stringify({
          name,
          email,
          password,
          tenant_slug:
            "dmart-india",
          store_id: 4,
        }),
      }
    );

    const data =
      await response.json();

    if (response.ok) {
      alert(
        "Registration successful. Verify email."
      );

      router.push(
        "/auth/verify-email"
      );
    } else {
      alert(
        JSON.stringify(data)
      );
    }
  };

  return (
    <div className="login-container">
      <div className="left-panel">
        <form
          className="login-form"
          onSubmit={register}
        >
          <h1>
            Retail Store Register
          </h1>

          <div className="input-group">
            <input
              placeholder="Name"
              value={name}
              onChange={(e) =>
                setName(
                  e.target.value
                )
              }
            />
          </div>

          <div className="input-group">
            <input
              placeholder="Email"
              value={email}
              onChange={(e) =>
                setEmail(
                  e.target.value
                )
              }
            />
          </div>

          <div className="input-group">
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
          </div>

          <button
            className="login-btn"
            type="submit"
          >
            Register
          </button>
        </form>
      </div>

      <div className="right-panel">
        <h2>Retail Store</h2>
      </div>
    </div>
  );
}