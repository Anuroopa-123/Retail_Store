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
    <div>

      <h1>
        Verify Email
      </h1>

      <input
        value={otp}
        onChange={(e)=>
          setOtp(
            e.target.value
          )
        }
        placeholder="Enter OTP"
      />

      <button
        onClick={verifyOTP}
      >
        Verify
      </button>

    </div>
  );
}