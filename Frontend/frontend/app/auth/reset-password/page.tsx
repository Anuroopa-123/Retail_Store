"use client";

import { useState } from "react";

export default function ResetPasswordPage() {

  const [token, setToken] =
    useState("");

  const [password,
    setPassword] =
      useState("");

  const reset = async () => {

    const response =
      await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/reset-password`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            token,
            new_password:
              password,
          }),
        }
      );

    const data =
      await response.json();

    alert(
      data.message ||
      data.detail
    );
  };

  return (
    <div className="login-container">

      <div className="left-panel">

        <div className="login-form">

          <h1>
            Reset Password
          </h1>

          <div className="input-group">
            <input
              placeholder="Token"
              value={token}
              onChange={(e) =>
                setToken(
                  e.target.value
                )
              }
            />
          </div>

          <div className="input-group">
            <input
              type="password"
              placeholder="New Password"
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
            onClick={reset}
          >
            Reset Password
          </button>

        </div>

      </div>

      <div className="right-panel">
        <h2>
          Retail Store
        </h2>
      </div>

    </div>
  );
}