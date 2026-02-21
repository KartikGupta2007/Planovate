// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Register Page
// ============================================

import React, { useState } from "react";
// TODO: import { register } from "../appwrite/auth";
// TODO: import { useNavigate } from "react-router-dom";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    // TODO: Implement registration logic using Appwrite auth
    // const result = await register(name, email, password);
    // if (result.success) navigate("/login");
  };

  return (
    <div className="register-page">
      <h2>Create Account</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
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
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
