"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import "./login.css";
import { generateCaptcha } from "@/src/lib/captcha";
import {
  useAuth
} from "@/src/context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const {
  redirectToDashboard
} = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [captcha, setCaptcha] = useState(
    () => generateCaptcha()
  );

  const [userCaptcha, setUserCaptcha] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleLogin = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    if (userCaptcha !== captcha) {
      alert("Invalid Captcha");

      setCaptcha(
        generateCaptcha()
      );

      setUserCaptcha("");

      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            email,
            password,
          }),
        }
      );

      const data =
        await response.json();

  if (response.ok) {

  localStorage.setItem(
    "access_token",
    data.access_token
  );

  localStorage.setItem(
    "refresh_token",
    data.refresh_token
  );

  const meResponse =
    await fetch(
      "http://127.0.0.1:8000/api/v1/auth/me",
      {
        headers: {
          Authorization:
            `Bearer ${data.access_token}`
        }
      }
    );

  const currentUser =
    await meResponse.json();

  redirectToDashboard(
    currentUser
  );
} else {
      if (
  response.status === 403 &&
  data.detail.includes("verified")
) {

  router.push(
    "/auth/verify-email"
  );

  return;
}

alert(data.detail);
      }
    } catch (error) {
      console.error(error);

      alert(
        "Unable to connect to server"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">

      {/* LEFT PANEL */}

      <div className="left-panel">

        <div className="brand-content">

          <div className="brand-logo">

            <div className="logo-icon">
              🛍️
            </div>

            <span className="logo-text">
              Retail
              <span>IQ</span>
            </span>

          </div>

          <h1 className="brand-headline">
            Run your store
            <br />
            <em>
              smarter, faster.
            </em>
          </h1>

          <p className="brand-sub">
            One platform to manage
            tenants, inventory,
            staff, and sales —
            with AI-powered insights.
          </p>

          <div className="stat-cards">

            <div className="stat-card">
              <span className="stat-number stat-accent">
                98%
              </span>

              <span className="stat-label">
                Uptime
              </span>
            </div>

            <div className="stat-card">
              <span className="stat-number">
                12k+
              </span>

              <span className="stat-label">
                Stores
              </span>
            </div>

            <div className="stat-card">
              <span className="stat-number stat-accent">
                4.9★
              </span>

              <span className="stat-label">
                Rating
              </span>
            </div>

          </div>

        </div>

      </div>

      {/* RIGHT PANEL */}

      <div className="right-panel">

        <div className="form-container">

          <span className="form-eyebrow">
            Super Admin Portal
          </span>

          <h2 className="form-title">
            Welcome back
          </h2>

          <p className="form-subtitle">
            Sign in to manage your
            retail network
          </p>

          <form
            className="login-form"
            onSubmit={handleLogin}
          >

            {/* EMAIL */}

            <div className="input-wrapper">

              <label className="input-label">
                Email Address
              </label>

              <span className="input-icon">
                ✉️
              </span>

              <input
                className="input-field"
                type="email"
                placeholder="admin@retailiq.com"
                value={email}
                onChange={(e) =>
                  setEmail(
                    e.target.value
                  )
                }
                required
              />

            </div>

            {/* PASSWORD */}

            <div className="input-wrapper">

              <label className="input-label">
                Password
              </label>

              <span className="input-icon">
                🔒
              </span>

              <input
                className="input-field"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) =>
                  setPassword(
                    e.target.value
                  )
                }
                required
              />

            </div>

            {/* CAPTCHA */}

            <div
              className="input-wrapper"
            >

              <label className="input-label">
                Security Verification
              </label>

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  alignItems:
                    "center",
                  marginBottom:
                    "12px",
                }}
              >

                <div
                  className="captcha-text"
                >
                  {captcha}
                </div>

                <button
                  type="button"
                  className="login-btn"
                  style={{
                    width: "120px",
                    padding: "12px",
                    marginTop: 0,
                  }}
                  onClick={() =>
                    setCaptcha(
                      generateCaptcha()
                    )
                  }
                >
                  Refresh
                </button>

              </div>

              <input
                className="input-field"
                placeholder="Enter Captcha"
                value={userCaptcha}
                onChange={(e) =>
                  setUserCaptcha(
                    e.target.value
                  )
                }
                required
              />

            </div>

            <div className="forgot-row">

              <a
                href="/auth/forgot-password"
                className="forgot-link"
              >
                Forgot Password?
              </a>

            </div>

            <button
              className="login-btn"
              type="submit"
              disabled={loading}
            >
              <span>
                {loading
                  ? "Signing In..."
                  : "Sign In →"}
              </span>
            </button>

          </form>

        </div>

      </div>

    </div>
  );
}