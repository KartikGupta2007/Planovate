// ============================================
// COMPONENT: Before/After Showcase
// Displays a featured renovation project example
// ============================================

import React from "react";
import BeforeImage from "../assets/Before.jpeg";
import AfterImage from "../assets/After.jpeg";

const BeforeAfterShowcase = () => {
  const description = `Living Room Renovation – Budget Smart Upgrade

The original space showed major wall cracks (score 0.72), peeling paint (0.64), moisture-stained ceiling, and uneven lighting. Planovate prioritized structural repair and surface restoration first.

With a ₹100,000 budget, the system optimized the plan to include crack repair, waterproof repainting, and LED lighting upgrades while deferring flooring replacement to stay within limits.

The result is a smooth, crack-free finish, durable fresh paint, brighter balanced lighting, and a visibly modernized living space — all achieved through AI-driven cost and priority optimization.`;

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Lilita+One&display=swap');
        .showcase-title {
          font-family: 'Lilita One', 'Arial Black', sans-serif;
          -webkit-text-stroke: 2.5px #111;
          color: transparent;
          paint-order: stroke fill;
          letter-spacing: -1px;
        }
      `}</style>

      <div className="py-16" style={{ background: "#F4EFE4", borderTop: "3px solid #111" }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Section Header */}
          <div className="text-center mb-12">
            <h2 className="showcase-title text-5xl mb-4" style={{ lineHeight: "1.1" }}>
              SEE THE MAGIC
            </h2>
            <p className="text-base font-bold uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555", letterSpacing: "0.08em" }}>
              Real transformation powered by AI
            </p>
          </div>

          {/* Before/After Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
            {/* BEFORE */}
            <div className="bg-white border-2 border-black rounded-2xl overflow-hidden" style={{ boxShadow: "8px 8px 0px #111" }}>
              <div className="relative">
                <div className="absolute top-4 left-4 z-10">
                  <span className="inline-block px-4 py-2 rounded-full border-2 border-black font-black text-sm uppercase" style={{ background: "#FF6B6B", color: "#fff", fontFamily: "'Boogaloo', Arial, sans-serif", boxShadow: "3px 3px 0px #111" }}>
                    BEFORE
                  </span>
                </div>
                <img
                  src={BeforeImage}
                  alt="Living room before renovation"
                  className="w-full h-96 object-cover"
                />
              </div>
              <div className="p-6 border-t-2 border-black">
                <h3 className="text-xl font-black mb-2" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>
                  Original Space
                </h3>
                <ul className="text-sm space-y-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
                  <li>❌ Major wall cracks (score 0.72)</li>
                  <li>❌ Peeling paint (0.64)</li>
                  <li>❌ Moisture-stained ceiling</li>
                  <li>❌ Uneven lighting</li>
                </ul>
              </div>
            </div>

            {/* AFTER */}
            <div className="bg-white border-2 border-black rounded-2xl overflow-hidden" style={{ boxShadow: "8px 8px 0px #111" }}>
              <div className="relative">
                <div className="absolute top-4 left-4 z-10">
                  <span className="inline-block px-4 py-2 rounded-full border-2 border-black font-black text-sm uppercase" style={{ background: "#ADFF2F", color: "#111", fontFamily: "'Boogaloo', Arial, sans-serif", boxShadow: "3px 3px 0px #111" }}>
                    AFTER
                  </span>
                </div>
                <img
                  src={AfterImage}
                  alt="Living room after renovation"
                  className="w-full h-96 object-cover"
                />
              </div>
              <div className="p-6 border-t-2 border-black">
                <h3 className="text-xl font-black mb-2" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>
                  Transformed Space
                </h3>
                <ul className="text-sm space-y-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
                  <li>✅ Smooth, crack-free finish</li>
                  <li>✅ Durable fresh paint</li>
                  <li>✅ Brighter balanced lighting</li>
                  <li>✅ Modernized living space</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Description Card */}
          <div className="max-w-4xl mx-auto bg-white border-2 border-black rounded-2xl p-8" style={{ boxShadow: "8px 8px 0px #111" }}>
            <div className="flex items-start gap-4 mb-4">
              <div className="bg-lime-400 rounded-full p-3 border-2 border-black" style={{ boxShadow: "3px 3px 0px #111" }}>
                <svg className="w-6 h-6" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-black mb-3" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>
                  Project Success Story
                </h3>
                <div className="text-base leading-relaxed whitespace-pre-line" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#333", lineHeight: "1.7" }}>
                  {description}
                </div>
              </div>
            </div>

            {/* Budget Badge */}
            <div className="mt-6 pt-6 border-t-2 border-black">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div className="flex items-center gap-3">
                  <span className="text-xs font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
                    Total Budget:
                  </span>
                  <span className="text-3xl font-black" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>
                    ₹100,000
                  </span>
                </div>
                <div className="inline-block px-4 py-2 rounded-full border-2 border-black font-black text-xs uppercase" style={{ background: "#ADFF2F", fontFamily: "'Boogaloo', Arial, sans-serif", boxShadow: "3px 3px 0px #111" }}>
                  AI OPTIMIZED
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default BeforeAfterShowcase;
