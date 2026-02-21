// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Navbar Component
// ============================================

import React from "react";
// TODO: import { Link } from "react-router-dom";
// TODO: import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  // TODO: const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <h1>RenovAI</h1>
      <div className="nav-links">
        {/* TODO: Add navigation links */}
        {/* <Link to="/upload">New Project</Link> */}
        {/* <Link to="/history">History</Link> */}
        {/* {user ? <button onClick={logout}>Logout</button> : <Link to="/login">Login</Link>} */}
      </div>
    </nav>
  );
};

export default Navbar;
