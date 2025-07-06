
import React, { createContext, useState, useEffect, useCallback } from "react";

export const AuthContext = createContext(null);

/**
 * AuthProvider
 *  - stores JWT in localStorage
 *  - auto‑logs out when the token expires (uses expires_in from /login)
 *  - exposes helper fetch that attaches Authorization header
 */
export const AuthProvider = ({ children }) => {
  /** token & logout timer */
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const timerIdRef = React.useRef(null);

  /* ------------------------------------------------ timers */
  const clearTimer = () => {
    if (timerIdRef.current) clearTimeout(timerIdRef.current);
    timerIdRef.current = null;
  };
  const startTimer = (seconds) => {
    clearTimer();
    // fallback: if no seconds given, default 1h (3600)
    timerIdRef.current = setTimeout(() => logout(), (seconds || 3600) * 1000);
  };

  /* ------------------------------------------------ helper fetch */
  const authFetch = useCallback(
    (url, opts = {}) => {
      const headers = { ...(opts.headers || {}) };
      if (token) headers.Authorization = `Bearer ${token}`;
      return fetch(url, { ...opts, headers });
    },
    [token]
  );

  /* ------------------------------------------------ register / login / logout */
  const register = async (username, password) => {
    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    return res.ok;
  };

  const login = async (username, password) => {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) return false;
    const { access_token, expires_in } = await res.json();
    localStorage.setItem("token", access_token);
    setToken(access_token);
    startTimer(expires_in);
    return true;
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    clearTimer();
  };

  /* ------------------------------------------------ on mount */
  useEffect(() => {
    // If a token already exists in localStorage at load, assume ~55 min left
    if (token) startTimer(3300);
    return () => clearTimer();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <AuthContext.Provider
      value={{ token, register, login, logout, authFetch }}
    >
      {children}
    </AuthContext.Provider>
  );
};
