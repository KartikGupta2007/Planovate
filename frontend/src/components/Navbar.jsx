// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Navbar Component
// ============================================

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import authService from "../appwrite/auth";
import Logo from "../assets/Logo.jpeg";

const Navbar = () => {
  const { user, setUser } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await authService.logout();
      setUser(null);
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const navLinkStyle = {
    fontFamily: "'Boogaloo', Arial, sans-serif",
    fontWeight: 700,
    letterSpacing: "0.06em",
    textTransform: "uppercase",
    fontSize: "0.9rem",
    color: "#111",
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Lilita+One&family=Nunito:wght@900&display=swap');
        .nav-link:hover { text-decoration: underline; text-underline-offset: 4px; }
        .nav-logo {
          font-family: 'Lilita One', 'Arial Black', sans-serif;
          -webkit-text-stroke: 2px #111;
          paint-order: stroke fill;
          letter-spacing: -1px;
          line-height: 1;
        }
        .nav-logo-green {
          color: #ADFF2F;
        }
        .nav-logo-pink {
          color: #FF1F5A;
        }
        .nav-btn {
          font-family: 'Boogaloo', Arial, sans-serif;
          font-weight: 700;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          border: 2px solid #111;
          padding: 6px 18px;
          border-radius: 999px;
          font-size: 0.85rem;
          transition: transform 0.1s ease, box-shadow 0.1s ease;
        }
        .nav-btn:hover {
          transform: translate(-2px, -2px);
          box-shadow: 4px 4px 0px #111;
        }
        .nav-btn-outline {
          background: transparent;
          color: #111;
        }
        .nav-btn-fill {
          background: #ADFF2F;
          color: #111;
          box-shadow: 3px 3px 0px #111;
        }
        .nav-btn-danger {
          background: #FF1F5A;
          color: #fff;
          box-shadow: 3px 3px 0px #111;
        }
      `}</style>

      <nav style={{ background: "#F4EFE4", borderBottom: "3px solid #111" }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">

            {/* Logo */}
            <Link to="/" className="flex items-center gap-1">
              <img src={Logo} alt="Planovate Logo" className="h-14 w-14" style={{ borderRadius: "8px" }} />
              <span className="nav-logo" style={{ fontSize: "2rem" }}>
                <span className="nav-logo-green">Plano</span>
                <span className="nav-logo-pink">vate</span>
              </span>
            </Link>

            {/* Desktop Nav */}
            <div className="hidden md:flex items-center gap-6">
              {user && (
                <>
                  <Link to="/dashboard" className="nav-link" style={navLinkStyle}>Dashboard</Link>
                  <Link to="/upload" className="nav-link" style={navLinkStyle}>New Project</Link>
                </>
              )}

              {user ? (
                <div className="flex items-center gap-3">
                  <span
                    className="text-xs font-bold uppercase tracking-widest"
                    style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}
                  >
                    {user.name || user.email}
                  </span>
                  <button onClick={handleLogout} className="nav-btn nav-btn-danger">
                    Sign Out
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-3">
                  <Link to="/login" className="nav-btn nav-btn-outline">Sign In</Link>
                  <Link to="/register" className="nav-btn nav-btn-fill">Sign Up</Link>
                </div>
              )}
            </div>

            {/* Mobile hamburger */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden flex flex-col gap-1.5 p-1"
              aria-label="Toggle menu"
            >
              <span
                className="block w-6 h-0.5 transition-all duration-200"
                style={{
                  background: "#111",
                  transform: isMenuOpen ? "rotate(45deg) translate(4px, 4px)" : "none",
                }}
              />
              <span
                className="block w-6 h-0.5 transition-all duration-200"
                style={{
                  background: "#111",
                  opacity: isMenuOpen ? 0 : 1,
                }}
              />
              <span
                className="block w-6 h-0.5 transition-all duration-200"
                style={{
                  background: "#111",
                  transform: isMenuOpen ? "rotate(-45deg) translate(4px, -4px)" : "none",
                }}
              />
            </button>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden pb-5 pt-2 flex flex-col gap-3" style={{ borderTop: "2px solid #111" }}>
              {user && (
                <>
                  <Link to="/dashboard" className="nav-link" style={navLinkStyle} onClick={() => setIsMenuOpen(false)}>
                    Dashboard
                  </Link>
                  <Link to="/upload" className="nav-link" style={navLinkStyle} onClick={() => setIsMenuOpen(false)}>
                    New Project
                  </Link>
                </>
              )}

              {user ? (
                <>
                  <span className="text-xs font-bold uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
                    {user.name || user.email}
                  </span>
                  <button
                    onClick={() => { handleLogout(); setIsMenuOpen(false); }}
                    className="nav-btn nav-btn-danger w-fit"
                  >
                    Sign Out
                  </button>
                </>
              ) : (
                <div className="flex gap-3">
                  <Link to="/login" className="nav-btn nav-btn-outline" onClick={() => setIsMenuOpen(false)}>Sign In</Link>
                  <Link to="/register" className="nav-btn nav-btn-fill" onClick={() => setIsMenuOpen(false)}>Sign Up</Link>
                </div>
              )}
            </div>
          )}
        </div>
      </nav>
    </>
  );
};

export default Navbar;
