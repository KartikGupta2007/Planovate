// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Auth Context – Global Authentication State
// ============================================

import React, { createContext, useContext, useState, useEffect } from "react";
import authService from "../appwrite/auth";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    authService.getCurrentUser()
      .then((userData) => setUser(userData))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const value = {
    user,
    setUser,
    loading,
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
