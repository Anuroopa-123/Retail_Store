"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import "./verify-email.css";

export default function VerifyEmail() {

  const router = useRouter();

  const [email, setEmail] =
  useState("");

  const [otp, setOtp] =
    useState("");

  const verifyOTP =
    async () => {

      const response =
        await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/verify-otp?token=${otp}`,
          {
            method: "POST"
          }
        );

      const data =
        await response.json();

      alert(data.message);

      if(response.ok){

        router.push(
          "/auth/login"
        );

      }
  };

 return (
  <div className="verify-container">

    <div className="verify-card">

      <div className="verify-icon">
        📧
      </div>

      <h1 className="verify-title">
        Verify Email
      </h1>

      <p className="verify-subtitle">
        Enter the 6 digit OTP sent
        to your email address.
      </p>

      <input
        className="otp-input"
        value={otp}
        onChange={(e) =>
          setOtp(e.target.value)
        }
        placeholder="000000"
        maxLength={6}
      />

      <button
        className="verify-btn"
        onClick={verifyOTP}
      >
        Verify OTP
      </button>

    </div>

  </div>
);
}