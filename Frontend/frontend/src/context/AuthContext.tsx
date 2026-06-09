"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";

import { User } from "../types/user";
import { apiFetch } from "../lib/api/client";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  logout: () => void;
  refreshUser: () => Promise<void>;
  redirectToDashboard: (
    user: User
  ) => void;
}

const AuthContext =
  createContext<AuthContextType | null>(null);

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {

  const [user, setUser] =
    useState<User | null>(null);

  const [loading, setLoading] =
    useState(true);

  const redirectToDashboard =
    (user: User) => {

      if (
        user.roles?.includes(
          "super_admin"
        )
      ) {

        window.location.href =
          "/super-admin/dashboard";

      }

      else if (
        user.roles?.includes(
          "admin"
        )
      ) {

        window.location.href =
          "/admin/dashboard";

      }

      else if (
        user.roles?.includes(
          "employee"
        )
      ) {

        window.location.href =
          "/employee/dashboard";

      }

      else if (
        user.roles?.includes(
          "sales"
        )
      ) {

        window.location.href =
          "/sales/dashboard";

      }

      else {

        window.location.href =
          "/auth/login";

      }
  };

  const refreshUser = async () => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    if (!token) {
      setLoading(false);
      return;
    }

    try {

      const data =
        await apiFetch<User>(
          "/api/v1/auth/me"
        );

      setUser(data);

    } catch {

      localStorage.removeItem(
        "access_token"
      );

      localStorage.removeItem(
        "refresh_token"
      );

      setUser(null);

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {

    const timer =
      setTimeout(() => {

        void refreshUser();

      }, 0);

    return () =>
      clearTimeout(timer);

  }, []);

  const logout = () => {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "refresh_token"
    );

    setUser(null);

    window.location.href =
      "/auth/login";
  };

  return (

    <AuthContext.Provider
      value={{
        user,
        loading,
        logout,
        refreshUser,
        redirectToDashboard,
      }}
    >

      {children}

    </AuthContext.Provider>

  );
}

export const useAuth = () => {

  const context =
    useContext(AuthContext);

  if (!context) {

    throw new Error(
      "AuthContext missing"
    );

  }

  return context;
};