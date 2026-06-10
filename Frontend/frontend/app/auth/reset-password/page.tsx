"use client";

import {
useSearchParams,
useRouter
} from "next/navigation";

import { useState } from "react";
import toast from "react-hot-toast";
import "./reset-password.css";
import {
  FaEye,
  FaEyeSlash
} from "react-icons/fa";

export default function ResetPasswordPage() {

const params =
useSearchParams();

const router =
useRouter();
const [showPassword,
  setShowPassword] =
    useState(false);

const [showConfirmPassword,
  setShowConfirmPassword] =
    useState(false);
    const [passwordError,
  setPasswordError] =
    useState("");

const token =
params.get("token") || "";

const [password,
setPassword] =
useState("");

const [confirmPassword,
setConfirmPassword] =
useState("");

const [loading,
setLoading] =
useState(false);

const reset = async () => {


if (
  password !==
  confirmPassword
) {

  setPasswordError(
    "Passwords do not match"
  );

  return;
}

setPasswordError("");

setLoading(true);

try {

  const response =
    await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/reset-password`,
      {
        method:"POST",

        headers:{
          "Content-Type":
            "application/json",
        },

        body:JSON.stringify({
          token,
          new_password:
            password,
        }),
      }
    );

  const data =
    await response.json();

  if(!response.ok){

    toast.error(
      data.detail
    );

    return;
  }

  toast.success(
    "Password updated"
  );

  setTimeout(() => {

    router.push(
      "/auth/login"
    );

  },1500);

} catch(error){

  console.error(error);

  toast.error(
    "Something went wrong"
  );
} finally {

  setLoading(false);
}


};

return (


<div className="reset-container">

  <div className="reset-card">

    <div className="reset-icon">
      🔑
    </div>

    <h1>
      Reset Password
    </h1>

    <p>
      Enter your new password.
    </p>
<div className="input-group">

  <label>
    New Password
  </label>

  <div className="password-wrapper">

    <input
      type={
        showPassword
          ? "text"
          : "password"
      }
      placeholder="Enter New Password"
      value={password}
      onChange={(e) =>
        setPassword(
          e.target.value
        )
      }
    />

    <span
      className="eye-icon"
      onClick={() =>
        setShowPassword(
          !showPassword
        )
      }
    >
      {
        showPassword
          ? <FaEyeSlash />
          : <FaEye />
      }
    </span>

  </div>

</div>

<div className="input-group">

  <label>
    Confirm Password
  </label>

  <div className="password-wrapper">

    <input
      type={
        showConfirmPassword
          ? "text"
          : "password"
      }
      placeholder="Confirm Password"
      value={confirmPassword}
     onChange={(e) => {

  setConfirmPassword(
    e.target.value
  );

  if (
    password !==
    e.target.value
  ) {

    setPasswordError(
      "Passwords do not match"
    );

  } else {

    setPasswordError("");
  }
}}
    />

    <span
      className="eye-icon"
      onClick={() =>
        setShowConfirmPassword(
          !showConfirmPassword
        )
      }
    >
      {
        showConfirmPassword
          ? <FaEyeSlash />
          : <FaEye />
      }
    </span>

  </div>

</div>
{
  passwordError && (

    <div className="password-error">

      {passwordError}

    </div>

  )
}
    <button
      onClick={reset}
    >
      {
        loading
          ? "Updating..."
          : "Reset Password"
      }
    </button>

  </div>

</div>


);
}
