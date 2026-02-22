// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Login Page
// ============================================

import { useState } from "react";
import { useForm } from "react-hook-form";
import authService from "../../appwrite/auth.js";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.jsx";

function Login() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { setUser } = useAuth();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ mode: "onChange" });

  const onSubmit = async (data) => {
    setError("");
    setLoading(true);
    
    try {
      await authService.login({
        email: data.email,
        password: data.password
      });
      
      const userData = await authService.getCurrentUser();
      if (userData) {
        setUser(userData);
        navigate("/dashboard");
      }
    } catch (error) {
      setError(error.message || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Lilita+One&display=swap');
        .form-title {
          font-family: 'Lilita One', 'Arial Black', sans-serif;
          -webkit-text-stroke: 2px #111;
          color: transparent;
          paint-order: stroke fill;
          letter-spacing: -1px;
        }
        
        /* Blob animations */
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
          transition: transform 0.3s ease;
        }
        .blob-wrap:hover {
          transform: scale(1.12);
        }
      `}</style>
      
      <div className="relative flex items-center justify-center min-h-screen overflow-hidden" style={{ background: "#F4EFE4" }}>
        {/* Wireframe blobs */}
        <div className="absolute top-8 left-8 pointer-events-auto">
          <div className="blob-wrap" style={{ width: 180, height: 180 }}>
            <svg className="blob-A" width={180} height={180} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.88 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#8a6a30" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#8a6a30" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#8a6a30" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#8a6a30" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#8a6a30" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        <div className="absolute top-4 right-12 pointer-events-auto">
          <div className="blob-wrap" style={{ width: 220, height: 220 }}>
            <svg className="blob-B" width={220} height={220} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.87 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#1a9f90" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#1a9f90" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#1a9f90" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#1a9f90" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#1a9f90" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        <div className="absolute bottom-10 left-10 pointer-events-auto">
          <div className="blob-wrap" style={{ width: 160, height: 160 }}>
            <svg className="blob-C" width={160} height={160} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.86 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#c05540" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#c05540" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#c05540" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#c05540" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#c05540" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        <div className="absolute bottom-16 right-16 pointer-events-auto">
          <div className="blob-wrap" style={{ width: 190, height: 190 }}>
            <svg className="blob-D" width={190} height={190} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.88 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#7755aa" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#7755aa" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#7755aa" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#7755aa" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#7755aa" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        {/* Mid-left */}
        <div className="absolute top-[42%] left-[6%] pointer-events-auto hidden md:block">
          <div className="blob-wrap" style={{ width: 130, height: 130 }}>
            <svg className="blob-E" width={130} height={130} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.85 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#3366bb" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#3366bb" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#3366bb" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#3366bb" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#3366bb" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        {/* Mid-right */}
        <div className="absolute top-[38%] right-[5%] pointer-events-auto hidden md:block">
          <div className="blob-wrap" style={{ width: 145, height: 145 }}>
            <svg className="blob-F" width={145} height={145} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.85 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#b85530" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#b85530" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#b85530" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#b85530" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#b85530" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        {/* Upper-center-right */}
        <div className="absolute top-[14%] right-[28%] pointer-events-auto hidden lg:block">
          <div className="blob-wrap" style={{ width: 105, height: 105 }}>
            <svg className="blob-A" width={105} height={105} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.80 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#aa5588" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#aa5588" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#aa5588" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#aa5588" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#aa5588" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        {/* Lower-center */}
        <div className="absolute bottom-[22%] left-[38%] pointer-events-auto hidden lg:block">
          <div className="blob-wrap" style={{ width: 115, height: 115 }}>
            <svg className="blob-D" width={115} height={115} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.80 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#0077aa" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#0077aa" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#0077aa" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#0077aa" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#0077aa" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        {/* Far top-center */}
        <div className="absolute top-[6%] left-[40%] pointer-events-auto hidden lg:block">
          <div className="blob-wrap" style={{ width: 90, height: 90 }}>
            <svg className="blob-E" width={90} height={90} viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ opacity: 0.78 }}>
              <ellipse cx="100" cy="100" rx="88" ry="88" stroke="#559900" strokeWidth="2.5"/>
              <ellipse cx="100" cy="100" rx="32" ry="32" stroke="#559900" strokeWidth="2"/>
              {[-55, -30, -8, 14, 36, 58].map((offset, i) => {
                const maxR = 88;
                const rx = Math.sqrt(Math.max(0, maxR * maxR - offset * offset));
                return <ellipse key={i} cx="100" cy={100 + offset} rx={rx} ry={rx * 0.28} stroke="#559900" strokeWidth="1.2" strokeDasharray="5 3" />;
              })}
              {[0, 36, 72, 108, 144].map((angle, i) => <ellipse key={i} cx="100" cy="100" rx="60" ry="88" stroke="#559900" strokeWidth="1.2" strokeDasharray="4 3" transform={`rotate(${angle}, 100, 100)`} />)}
              <ellipse cx="100" cy="100" rx="88" ry="25" stroke="#559900" strokeWidth="2"/>
            </svg>
          </div>
        </div>
        
        <div className="relative z-10 mx-auto w-full max-w-md bg-white p-8 border-2 border-black rounded-2xl" style={{ boxShadow: "8px 8px 0px #111" }}>
          <h2 className="form-title text-center text-5xl mb-2" style={{ lineHeight: "1.1" }}>
            SIGN IN
          </h2>
          <p className="mt-2 text-center text-sm font-bold uppercase mb-6" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", letterSpacing: "0.06em", color: "#555" }}>
            Don't have an account?&nbsp;
            <Link
              to="/register"
              className="underline text-pink-600 hover:text-pink-700"
            >
              Sign Up
            </Link>
          </p>
          
          {error && (
            <p className="font-bold uppercase tracking-wide text-sm px-4 py-3 rounded-lg mb-6 border-2 border-red-500 bg-red-50 text-red-700 text-center">
              {error}
            </p>
          )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-xs font-black uppercase tracking-widest mb-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="Enter your email"
                {...register("email", {
                  required: "Email is required",
                  validate: {
                    matchPattern: (value) =>
                      /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) ||
                      "Email address must be a valid address",
                  },
                })}
                className="w-full px-3 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
              {errors.email && (
                <p className="text-red-600 text-xs mt-1 font-semibold">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="block text-xs font-black uppercase tracking-widest mb-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  {...register("password", {
                    required: "Password is required",
                  })}
                  className="w-full px-3 py-2 pr-10 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-gray-100 rounded transition-colors"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5 text-gray-600">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5 text-gray-600">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="text-red-600 text-xs mt-1 font-semibold">{errors.password.message}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              style={{
                background: loading ? "#ccc" : "#ADFF2F",
                boxShadow: loading ? "none" : "4px 4px 0px #111",
                fontFamily: "'Boogaloo', Arial, sans-serif",
                letterSpacing: "0.1em",
                color: "#111"
              }}
            >
              {loading ? "LOGGING IN..." : "LOGIN →"}
            </button>
          </div>
        </form>
      </div>
    </div>
    </>
  );
}

export default Login;