"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import "./verify-reset-otp.css";

export default function VerifyResetOtpPage() {

const router = useRouter();

const [otp, setOtp] =
useState("");

const [loading, setLoading] =
useState(false);

const verifyOtp = async () => {


if (!otp) {

  toast.error(
    "Enter OTP"
  );

  return;
}

setLoading(true);

try {

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
