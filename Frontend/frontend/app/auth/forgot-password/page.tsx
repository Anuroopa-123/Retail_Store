"use client";

import { useState } from "react";

export default function ForgotPasswordPage() {

  const [email, setEmail] =
    useState("");

  const submit = async () => {

    const response =
      await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/forgot-password`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            email,
          }),
        }
      );

    const data =
      await response.json();

    alert(
      data.message
    );
  };

  return (
    <div className="login-container">

      <div className="left-panel">

        <div className="login-form">

          <h1>
            Forgot Password
          </h1>

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

          <button
            className="login-btn"
            onClick={submit}
          >
            Send Reset Link
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