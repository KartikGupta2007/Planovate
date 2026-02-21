// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Auth Context – Global Authentication State
// ============================================

import React, { createContext, useContext, useState, useEffect } from "react";
// TODO: import { getCurrentUser, login, logout, register } from "../appwrite/auth";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Check if user is already logged in
    // getCurrentUser().then(setUser).catch(() => setUser(null)).finally(() => setLoading(false));
    setLoading(false);
  }, []);

  const value = {
    user,
    loading,
    // TODO: Expose login, logout, register functions
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
