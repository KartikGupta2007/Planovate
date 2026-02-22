// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Dashboard – Shows User's Renovation Projects
// ============================================

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import service from "../../appwrite/service";
import BeforeAfterShowcase from "../BeforeAfterShowcase";

/* ── Keyframes & custom styles injected once ── */
const HeroStyles = () => (
  <style>{`
    @import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Lilita+One&family=Nunito:wght@900&display=swap');

    .hero-outline {
      font-family: 'Lilita One', 'Arial Black', sans-serif;
      font-weight: 900;
      -webkit-text-stroke: 4px #111;
      color: transparent;
      line-height: 0.88;
      letter-spacing: -1px;
      paint-order: stroke fill;
    }
    .hero-fill {
      font-family: 'Lilita One', 'Arial Black', sans-serif;
      font-weight: 900;
      color: #FF1F5A;
      -webkit-text-stroke: 7px #111;
      paint-order: stroke fill;
      text-shadow: 8px 8px 0px #111;
      line-height: 0.85;
      letter-spacing: -2px;
      transition: color 0.1s ease;
    }
    @keyframes color-flash {
      0%, 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100% { 
        color: #FF1F5A;
        transform: translate(0, 0);
      }
      5% { 
        color: #0066FF;
        transform: translate(2px, -2px);
      }
      15% { 
        color: #0066FF;
        transform: translate(-2px, 2px);
      }
      25% { 
        color: #0066FF;
        transform: translate(2px, 2px);
      }
      35% { 
        color: #0066FF;
        transform: translate(-2px, -2px);
      }
      45% { 
        color: #0066FF;
        transform: translate(3px, -1px);
      }
      55% { 
        color: #0066FF;
        transform: translate(-1px, 3px);
      }
      65% { 
        color: #0066FF;
        transform: translate(2px, -3px);
      }
      75% { 
        color: #0066FF;
        transform: translate(-3px, 2px);
      }
      85% { 
        color: #0066FF;
        transform: translate(1px, -2px);
      }
      95% { 
        color: #0066FF;
        transform: translate(-2px, 1px);
      }
    }
    .hero-text-container:hover .hero-fill {
      animation: color-flash 1.5s linear forwards;
    }
    .badge-float {
      font-family: 'Boogaloo', 'Arial', sans-serif;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      border: 2px solid #111;
      padding: 6px 14px;
      cursor: default;
      user-select: none;
    }
    .marquee-track {
      display: flex;
      white-space: nowrap;
      animation: marquee-scroll 18s linear infinite;
      gap: 0;
    }
    @keyframes marquee-scroll {
      from { transform: translateX(0); }
      to   { transform: translateX(-50%); }
    }
    .project-card:hover {
      transform: translateY(-4px);
      transition: transform 0.2s ease;
    }

    /* ── Wireframe blob animations ── */
    @keyframes blob-spinA {
      0%   { transform: rotate3d(1, 0.6, 0.3, 0deg) scale(1); }
      100% { transform: rotate3d(1, 0.6, 0.3, 360deg) scale(1); }
    }
    @keyframes blob-spinB {
      0%   { transform: rotate3d(0.4, 1, 0.5, 0deg) scale(1); }
      100% { transform: rotate3d(0.4, 1, 0.5, 360deg) scale(1); }
    }
    @keyframes blob-spinC {
      0%   { transform: rotate3d(0.7, 0.3, 1, 0deg) scale(1); }
      100% { transform: rotate3d(0.7, 0.3, 1, 360deg) scale(1); }
    }
    @keyframes blob-spinD {
      0%   { transform: rotate3d(1, 1, 0.2, 0deg) scale(1); }
      100% { transform: rotate3d(1, 1, 0.2, 360deg) scale(1); }
    }
    .blob-A { animation: blob-spinA 10s linear infinite; }
    .blob-B { animation: blob-spinB 14s linear infinite; }
    .blob-C { animation: blob-spinC 9s linear infinite reverse; }
    .blob-D { animation: blob-spinD 16s linear infinite; }
    .blob-E { animation: blob-spinA 12s linear infinite reverse; }
    .blob-F { animation: blob-spinC 7s linear infinite; }

    .blob-wrap:hover .blob-A { animation-duration: 2.5s; }
    .blob-wrap:hover .blob-B { animation-duration: 3.5s; }
    .blob-wrap:hover .blob-C { animation-duration: 2s; }
    .blob-wrap:hover .blob-D { animation-duration: 4s; }
    .blob-wrap:hover .blob-E { animation-duration: 2s; }
    .blob-wrap:hover .blob-F { animation-duration: 1.5s; }

    .blob-wrap {
      cursor: pointer;
      transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .blob-wrap:hover {
      transform: scale(1.25);
      filter: brightness(1.15) contrast(1.1);
    }
  `}</style>
);

/* ── Wireframe torus/blob SVG ── */
const WireframeBlob = ({ size = 180, stroke = "#111", opacity = 0.7, spinClass = "blob-A" }) => (
  <div className="blob-wrap" style={{ width: size, height: size }}>
    <svg
      className={spinClass}
      width={size}
      height={size}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ opacity }}
    >
      {/* Outer torus ring */}
      <ellipse cx="100" cy="100" rx="88" ry="88" stroke={stroke} strokeWidth="2.5"/>
      {/* Inner hole */}
      <ellipse cx="100" cy="100" rx="32" ry="32" stroke={stroke} strokeWidth="2"/>
      {/* Latitude cross-sections */}
      {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
        const maxR = 88;
        const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
        return (
          <ellipse
            key={i}
            cx="100"
            cy={100 + offset}
            rx={rx}
            ry={rx * 0.28}
            stroke={stroke}
            strokeWidth="1.2"
            strokeDasharray="5 3"
          />
        );
      })}
      {/* Longitude lines through the tube */}
      {[0, 36, 72, 108, 144].map((angle, i) => (
        <ellipse
          key={i}
          cx="100"
          cy="100"
          rx="60"
          ry="88"
          stroke={stroke}
          strokeWidth="1.2"
          strokeDasharray="4 3"
          transform={`rotate(${angle}, 100, 100)`}
        />
      ))}
      {/* Equator highlight */}
      <ellipse cx="100" cy="100" rx="88" ry="25" stroke={stroke} strokeWidth="2"/>
    </svg>
  </div>
);

const Dashboard = () => {
  const { user, loading: authLoading } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProjects = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        // Fetch only current user's projects
        const response = await service.getUserRows(user.$id);
        if (response?.rows) {
          setProjects(response.rows);
        } else if (response?.documents) {
          setProjects(response.documents);
        } else if (Array.isArray(response)) {
          setProjects(response);
        }
      } catch (error) {
        console.error("Error fetching projects:", error);
        setError("Failed to load projects. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (!authLoading) {
      fetchProjects();
    }
  }, [user, authLoading]);

  const getImageUrl = (fileId) => {
    if (!fileId) return null;
    return service.getFileView(fileId);
  };

  /* ── Loading ── */
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen" style={{ background: "#F4EFE4" }}>
        <HeroStyles />
        <p className="hero-outline text-5xl">LOADING...</p>
      </div>
    );
  }

  /* ── Not logged in → Parapixel-style hero ── */
  if (!user) {
    const marqueeText = Array(12).fill("⚠ CAUTION: RENOVATION OVERLOAD  ").join("");
    return (
      <div style={{ background: "#F4EFE4" }}>
        <HeroStyles />
        
        {/* Hero Section */}
        <div className="relative min-h-screen overflow-hidden">
          {/* ── Wireframe 3D blobs ── */}
          {/* Top-left */}
          <div className="absolute top-4 left-4 pointer-events-auto">
            <WireframeBlob size={210} stroke="#8a6a30" opacity={0.92} spinClass="blob-A" />
          </div>
          {/* Top-right */}
          <div className="absolute top-2 right-6 pointer-events-auto">
            <WireframeBlob size={250} stroke="#1a9f90" opacity={0.90} spinClass="blob-B" />
          </div>
          {/* Bottom-left */}
          <div className="absolute bottom-16 left-6 pointer-events-auto">
            <WireframeBlob size={195} stroke="#c05540" opacity={0.90} spinClass="blob-C" />
          </div>
          {/* Bottom-right */}
          <div className="absolute bottom-12 right-8 pointer-events-auto">
            <WireframeBlob size={175} stroke="#7755aa" opacity={0.90} spinClass="blob-D" />
          </div>
          {/* Mid-left */}
          <div className="absolute top-[42%] left-[6%] pointer-events-auto hidden md:block">
            <WireframeBlob size={130} stroke="#b85530" opacity={0.85} spinClass="blob-E" />
          </div>
          {/* Mid-right */}
          <div className="absolute top-[38%] right-[5%] pointer-events-auto hidden md:block">
            <WireframeBlob size={145} stroke="#3366bb" opacity={0.85} spinClass="blob-F" />
          </div>
          {/* Upper-center-right */}
          <div className="absolute top-[14%] right-[28%] pointer-events-auto hidden lg:block">
            <WireframeBlob size={105} stroke="#559900" opacity={0.80} spinClass="blob-A" />
          </div>
          {/* Lower-center */}
          <div className="absolute bottom-[22%] left-[38%] pointer-events-auto hidden lg:block">
            <WireframeBlob size={115} stroke="#aa5588" opacity={0.80} spinClass="blob-D" />
          </div>
          {/* Far top-center */}
          <div className="absolute top-[6%] left-[40%] pointer-events-auto hidden lg:block">
            <WireframeBlob size={90} stroke="#0077aa" opacity={0.78} spinClass="blob-E" />
          </div>

          {/* ── Floating badge stickers ── */}
          <div className="badge-float absolute top-20 left-10 bg-cyan-400" style={{ transform: "rotate(-8deg)" }}>★ AI POWERED</div>
          <div className="badge-float absolute top-28 right-16 bg-yellow-300" style={{ transform: "rotate(5deg)" }}>100% SMART</div>
          <div className="badge-float absolute bottom-40 left-12 bg-white" style={{ transform: "rotate(3deg)" }}>NO GUESSWORK</div>
          <div className="badge-float absolute bottom-52 right-10 bg-orange-400" style={{ transform: "rotate(-4deg)" }}>FULLY COSTED</div>
          <div className="badge-float absolute top-1/2 right-8 bg-violet-300" style={{ transform: "rotate(6deg) translateY(-80px)" }}>PURE MAGIC</div>

          {/* ── Hero text ── */}
          <div className="flex flex-col items-center justify-center min-h-screen pb-24 px-4 text-center">
            <div className="hero-text-container">
              <p className="hero-outline" style={{ fontSize: "clamp(3.5rem, 12vw, 10rem)" }}>WE FIX,</p>
              <p className="hero-fill" style={{ fontSize: "clamp(5rem, 17vw, 14rem)" }}>YOU FLEX</p>
            </div>

            {/* CTA */}
            <Link
              to="/register"
              className="mt-10 inline-block font-black text-lg uppercase tracking-widest px-10 py-4 rounded-full border-2 border-black"
              style={{
                background: "#ADFF2F",
                boxShadow: "4px 4px 0px #111",
                fontFamily: "'Boogaloo', Arial, sans-serif",
                letterSpacing: "0.12em",
              }}
            >
              START YOUR RENOVATION →
            </Link>

            <p className="mt-4 text-sm font-semibold" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", letterSpacing: "0.08em" }}>
              Already have an account?{" "}
              <Link to="/login" className="underline text-pink-600 hover:text-pink-700">Sign In</Link>
            </p>
          </div>

          {/* ── Bottom Marquee ticker ── */}
          <div
            className="absolute bottom-0 left-0 right-0 overflow-hidden py-3"
            style={{ background: "#FFE600", borderTop: "3px solid #111" }}
          >
            <div className="marquee-track">
              <span className="text-sm font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                {marqueeText}
              </span>
              <span className="text-sm font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                {marqueeText}
              </span>
            </div>
          </div>
        </div>

        {/* ── Before/After Showcase Section ── */}
        <BeforeAfterShowcase />
      </div>
    );
  }

  /* ── Logged-in dashboard ── */
  return (
    <div className="min-h-screen" style={{ background: "#F4EFE4" }}>
      <HeroStyles />

      {/* ── Bold hero banner ── */}
      <div className="relative overflow-hidden" style={{ borderBottom: "3px solid #111" }}>
        {/* Wireframe blobs */}
        <div className="absolute top-[15%] left-[12%] pointer-events-auto z-1">
          <WireframeBlob size={160} stroke="#8a6a30" opacity={0.88} spinClass="blob-A" />
        </div>
        <div className="absolute top-[8%] right-[18%] pointer-events-auto z-1">
          <WireframeBlob size={180} stroke="#1a9f90" opacity={0.87} spinClass="blob-B" />
        </div>
        <div className="absolute bottom-[22%] left-[25%] pointer-events-auto hidden md:block z-1">
          <WireframeBlob size={140} stroke="#c05540" opacity={0.86} spinClass="blob-C" />
        </div>
        <div className="absolute bottom-[18%] right-[28%] pointer-events-auto hidden md:block z-1">
          <WireframeBlob size={150} stroke="#7755aa" opacity={0.88} spinClass="blob-D" />
        </div>
        <div className="absolute top-[45%] left-[35%] pointer-events-auto hidden lg:block z-1">
          <WireframeBlob size={100} stroke="#3366bb" opacity={0.82} spinClass="blob-E" />
        </div>
        <div className="absolute top-[50%] right-[22%] pointer-events-auto hidden lg:block z-1">
          <WireframeBlob size={110} stroke="#b85530" opacity={0.83} spinClass="blob-F" />
        </div>
        
        <div className="badge-float absolute top-6 right-8 bg-cyan-400 hidden md:block z-10" style={{ transform: "rotate(4deg)" }}>AI POWERED</div>
        <div className="badge-float absolute bottom-10 right-36 bg-yellow-300 hidden md:block z-10" style={{ transform: "rotate(-3deg)" }}>PURE MAGIC</div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
          <p className="hero-outline" style={{ fontSize: "clamp(2.5rem, 7vw, 6rem)" }}>YOUR</p>
          <p className="hero-fill" style={{ fontSize: "clamp(3.5rem, 10vw, 8.5rem)" }}>PROJECTS</p>
          <p className="mt-3 text-base font-bold uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
            Welcome back, {user.name || user.email}
          </p>
        </div>

        {/* Mini marquee inside header */}
        <div className="overflow-hidden py-2" style={{ background: "#FFE600", borderTop: "2px solid #111" }}>
          <div className="marquee-track">
            {Array(16).fill(null).map((_, i) => (
              <span key={i} className="text-xs font-black uppercase px-4" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111", whiteSpace: "nowrap" }}>
                ✦ NEW PROJECT &nbsp;&nbsp; ✦ YOUR HISTORY &nbsp;&nbsp; ✦ AI ANALYSIS &nbsp;&nbsp;
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Background blobs for content area */}
        <div className="absolute top-20 right-[20%] pointer-events-auto hidden xl:block z-1">
          <WireframeBlob size={120} stroke="#aa5588" opacity={0.75} spinClass="blob-A" />
        </div>
        <div className="absolute bottom-32 left-[18%] pointer-events-auto hidden xl:block z-1">
          <WireframeBlob size={95} stroke="#0077aa" opacity={0.73} spinClass="blob-D" />
        </div>
        <div className="absolute top-[55%] right-[8%] pointer-events-auto hidden 2xl:block z-1">
          <WireframeBlob size={85} stroke="#559900" opacity={0.70} spinClass="blob-C" />
        </div>
        
        {/* New Project Button */}
        <div className="mb-8 relative z-10">
          <Link
            to="/upload"
            className="inline-flex items-center font-black text-base uppercase tracking-widest px-8 py-4 rounded-full border-2 border-black"
            style={{
              background: "#ADFF2F",
              boxShadow: "4px 4px 0px #111",
              fontFamily: "'Boogaloo', Arial, sans-serif",
              letterSpacing: "0.1em",
            }}
          >
            + NEW RENOVATION
          </Link>
        </div>

        {/* Error Message */}
        {error && (
          <div className="font-bold uppercase tracking-wide text-sm px-4 py-3 rounded-lg mb-6 border-2 border-red-500 bg-red-50 text-red-700">
            {error}
          </div>
        )}

        {/* Projects Section */}
        <div className="relative z-10">
          <p
            className="font-black uppercase mb-6"
            style={{ fontFamily: "'Boogaloo', Arial, sans-serif", fontSize: "clamp(1.2rem, 3vw, 2rem)", letterSpacing: "0.08em", color: "#111" }}
          >
            — YOUR RENOVATION HISTORY
          </p>

          {loading ? (
            <div className="flex items-center justify-center py-16">
              <p className="hero-outline" style={{ fontSize: "3rem" }}>LOADING...</p>
            </div>
          ) : projects.length === 0 ? (
            <div className="text-center py-16 border-2 border-black rounded-2xl" style={{ background: "#fff" }}>
              <p className="hero-outline mb-2" style={{ fontSize: "clamp(2rem, 6vw, 4rem)" }}>NOTHING YET</p>
              <p className="mb-6 font-semibold uppercase tracking-widest text-sm" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#777" }}>
                Start your first renovation project to see it here!
              </p>
              <Link
                to="/upload"
                className="inline-block font-black text-sm uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black"
                style={{
                  background: "#FF1F5A",
                  color: "#fff",
                  boxShadow: "4px 4px 0px #111",
                  fontFamily: "'Boogaloo', Arial, sans-serif",
                }}
              >
                CREATE FIRST PROJECT →
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project, index) => (
                <Link
                  key={project.$id || index}
                  to={`/project/${project.$id}`}
                  className="project-card block overflow-hidden border-2 border-black rounded-2xl"
                  style={{ background: "#fff", boxShadow: "5px 5px 0px #111" }}
                >
                  {/* Project Images */}
                  <div className="grid grid-cols-2 gap-0">
                    <div className="relative">
                      <p className="absolute top-2 left-2 text-xs font-black uppercase px-2 py-0.5 rounded-full border border-black z-10"
                        style={{ background: "#ADFF2F", fontFamily: "'Boogaloo', Arial, sans-serif" }}>
                        BEFORE
                      </p>
                      {project.CurrentPhoto ? (
                        <img
                          src={getImageUrl(project.CurrentPhoto)}
                          alt="Current state"
                          className="w-full h-36 object-cover"
                          onError={(e) => { e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/></svg>'; }}
                        />
                      ) : (
                        <div className="w-full h-36 flex items-center justify-center" style={{ background: "#eee" }}>
                          <span className="text-xs text-gray-400 font-bold uppercase">No image</span>
                        </div>
                      )}
                    </div>

                    <div className="relative" style={{ borderLeft: "2px solid #111" }}>
                      <p className="absolute top-2 left-2 text-xs font-black uppercase px-2 py-0.5 rounded-full border border-black z-10"
                        style={{ background: "#FF1F5A", color: "#fff", fontFamily: "'Boogaloo', Arial, sans-serif" }}>
                        AFTER
                      </p>
                      {project.Idealphoto ? (
                        <img
                          src={getImageUrl(project.Idealphoto)}
                          alt="Final result"
                          className="w-full h-36 object-cover"
                          onError={(e) => { e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/></svg>'; }}
                        />
                      ) : (
                        <div className="w-full h-36 flex items-center justify-center" style={{ background: "#eee" }}>
                          <span className="text-xs text-gray-400 font-bold uppercase">No image</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Project Details */}
                  <div className="p-4 border-t-2 border-black">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#777" }}>BUDGET</span>
                      <span className="font-black text-xl" style={{ color: "#FF1F5A", fontFamily: "'Nunito', Arial, sans-serif" }}>
                        ₹{project.Budget?.toLocaleString() || "N/A"}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2 font-medium">
                      {project.Description || "No description provided"}
                    </p>
                    {project.$createdAt && (
                      <p className="mt-2 text-xs font-bold uppercase tracking-wide" style={{ color: "#aaa", fontFamily: "'Boogaloo', Arial, sans-serif" }}>
                        {new Date(project.$createdAt).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
                      </p>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

