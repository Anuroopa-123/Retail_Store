"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import "./forgot-password.css";

export default function ForgotPasswordPage() {

const router = useRouter();

const [email, setEmail] =
useState("");

const [loading, setLoading] =
useState(false);

const handleSubmit = async (
e: React.FormEvent
) => {

e.preventDefault();

setLoading(true);

try {

  const response =
    await fetch(
      "http://127.0.0.1:8000/api/v1/auth/forgot-password",
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

  if (!response.ok) {

    toast.error(
      data.detail ||
      "Failed to send OTP"
    );

    return;
  }

  toast.success(
    "OTP sent to your email"
  );

  setTimeout(() => {

   router.push(
  `/auth/verify-reset-otp?email=${email}`
);

  }, 1500);

} catch (error) {

  console.error(error);

  toast.error(
    "Unable to connect to server"
  );
} finally {

  setLoading(false);
}


};

return (

<div className="forgot-container">

  <div className="forgot-card">

    <div className="forgot-icon">
      🔑
    </div>

    <h1>
      Forgot Password
    </h1>

    <p>
      Enter your registered email
      address and we will send a
      verification code.
    </p>

    <form
      onSubmit={handleSubmit}
    >

      <div className="input-group">

        <label>
          Email Address
        </label>

        <input
          type="email"
          placeholder="john@example.com"
          value={email}
          onChange={(e) =>
            setEmail(
              e.target.value
            )
          }
          required
        />

      </div>

      <button
        type="submit"
        disabled={loading}
      >

        {loading
          ? "Sending OTP..."
          : "Send OTP"}

      </button>

    </form>

  </div>

</div>


);
}
