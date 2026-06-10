"use client";

import { useState,useEffect } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import "./verify-reset-otp.css";

export default function VerifyResetOtpPage() {

const router = useRouter();

const [otp, setOtp] =
useState("");
const [timeLeft,
  setTimeLeft] =
    useState(120); // 2 mins

const [loading, setLoading] =
useState(false);

useEffect(() => {

  if (timeLeft <= 0) {

    toast.error(
      "OTP Expired"
    );

    router.push(
      "/auth/forgot-password"
    );

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

const verifyOtp = async () => {

  if (!otp) {

    toast.error(
      "Enter OTP"
    );

    return;
  }

  setLoading(true);

  try {

    const response =
      await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/reset-password?token=${otp}`
      );

    const data =
      await response.json();

    if (!response.ok) {

      toast.error(
        data.detail
      );

      return;
    }

    toast.success(
      "OTP Verified"
    );

    router.push(
      `/auth/reset-password?token=${otp}`
    );

  } catch (error) {

    console.error(error);

    toast.error(
      "OTP verification failed"
    );

  } finally {

    setLoading(false);
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
      🔐
    </div>

    <h1>
      Verify OTP
    </h1>

    <p>
      Enter the OTP sent to
      your email address.
    </p>
    <div className="otp-timer">

  OTP expires in

  <span>

    {String(minutes)
      .padStart(2,"0")}

    :

    {String(seconds)
      .padStart(2,"0")}

  </span>

</div>

    <input
      type="text"
      placeholder="Enter OTP"
      value={otp}
      onChange={(e) =>
        setOtp(
          e.target.value
        )
      }
    />

    <button
      onClick={verifyOtp}
      disabled={loading}
    >
      {
        loading
          ? "Verifying..."
          : "Verify OTP"
      }
    </button>

  </div>

</div>


);
}
