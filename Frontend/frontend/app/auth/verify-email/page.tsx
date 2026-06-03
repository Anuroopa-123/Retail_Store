"use client";

import {
  useEffect,
  useState,
} from "react";

import {
  useSearchParams,
  useRouter,
} from "next/navigation";

export default function VerifyEmail() {

  const searchParams =
    useSearchParams();

  const router =
    useRouter();

  const [message,
    setMessage] =
      useState("Verifying...");

  useEffect(() => {

    const token =
      searchParams.get("token");

    if (!token) return;

    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/verify-email?token=${token}`
    )
      .then((r) => r.json())
      .then((data) => {

        setMessage(
          data.message
        );

        setTimeout(() => {
          router.push(
            "/auth/login"
          );
        }, 3000);

      });

  }, [searchParams, router]);

  return (
    <div>
      <h1>
        {message}
      </h1>
    </div>
  );
}