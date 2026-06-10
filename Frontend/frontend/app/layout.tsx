import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

import {
  AuthProvider
} from "@/src/context/AuthContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "RetailIQ",
  description: "Retail Store Management",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (

    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable}`}
    >

      <body className="min-h-full flex flex-col">

        <Toaster
  position="top-right"
  toastOptions={{
    duration: 3000,

    success: {
      style: {
        background: "#22c55e",
        color: "#ffffff",
        borderRadius: "12px",
        padding: "14px 18px",
      },
      iconTheme: {
        primary: "#ffffff",
        secondary: "#22c55e",
      },
    },

    error: {
      style: {
        background: "#ef4444",
        color: "#ffffff",
        borderRadius: "12px",
        padding: "14px 18px",
      },
    },
  }}
/>


        <AuthProvider>

          {children}

        </AuthProvider>

      </body>

    </html>

  );
}