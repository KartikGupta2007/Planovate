// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Login Page
// ============================================

import React, { useState } from "react";
// TODO: import { login } from "../appwrite/auth";
// TODO: import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    // TODO: Implement login logic using Appwrite auth
    // const result = await login(email, password);
    // if (result.success) navigate("/dashboard");
  };

  return (
    <div className="login-page">
      <h2>Login to RenovAI</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
