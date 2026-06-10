"use client";

import { useState,useEffect } from "react";
import { useRouter } from "next/navigation";
import "./verify-email.css";

import toast from "react-hot-toast";


export default function VerifyEmail() {

  const router = useRouter();

  const [email, setEmail] =
  useState("");

  const [otp, setOtp] =
    useState("");
    const [timeLeft,
  setTimeLeft] =
    useState(60);

    useEffect(() => {

  if (timeLeft <= 0) {

    toast.error(
      "OTP Expired"
    );

    setTimeout(() => {

      router.push(
        "/auth/login"
      );

    }, 1000);

    return;
  }

  const timer =
    setInterval(() => {

      setTimeLeft(
        (prev) => prev - 1
      );

    }, 1000);

  return () =>
    clearInterval(timer);

}, [timeLeft, router]);




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

    if (response.ok) {

  toast.success(
    "Email verified successfully",
    {
      icon: "✅"
    }
  );

  setTimeout(() => {

    router.push(
      "/auth/login"
    );

  }, 1500);

} else {

  toast.error(
    data.detail ||
    "Invalid OTP"
  );

}

  

      
  };
  const minutes =
  Math.floor(
    timeLeft / 60
  );

const seconds =
  timeLeft % 60;

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
      <div className="otp-timer">

  OTP expires in

  <span>

    {String(minutes)
      .padStart(2, "0")}

    :

    {String(seconds)
      .padStart(2, "0")}

  </span>

</div>

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