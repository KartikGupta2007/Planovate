// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Project Detail View
// ============================================

import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import service from "../../appwrite/service";

const EachOldProject = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProject = async () => {
      if (!user) {
        navigate("/login");
        return;
      }

      try {
        setLoading(true);
        const response = await service.getRow(projectId);
        if (response) {
          setProject(response);
        } else {
          setError("Project not found");
        }
      } catch (error) {
        console.error("Error fetching project:", error);
        setError("Failed to load project details");
      } finally {
        setLoading(false);
      }
    };

    if (!authLoading) {
      fetchProject();
    }
  }, [projectId, user, authLoading, navigate]);

  const getImageUrl = (fileId) => {
    if (!fileId) return null;
    return service.getFileView(fileId);
  };

  // Loading state
  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen" style={{ background: "#F4EFE4" }}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-black mx-auto"></div>
          <p className="mt-4 text-xs font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>Loading project...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen py-8" style={{ background: "#F4EFE4" }}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white border-2 border-black rounded-lg p-6 text-center" style={{ boxShadow: "8px 8px 0px #111" }}>
            <svg
              className="mx-auto h-12 w-12 text-red-600 mb-4"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h2 className="text-3xl font-black mb-2" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>Error</h2>
            <p className="text-sm mb-4" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>{error}</p>
            <Link
              to="/dashboard"
              className="inline-block font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black"
              style={{ background: "#ADFF2F", boxShadow: "4px 4px 0px #111", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Project not found
  if (!project) {
    return (
      <div className="min-h-screen py-8" style={{ background: "#F4EFE4" }}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white border-2 border-black rounded-lg p-6 text-center" style={{ boxShadow: "8px 8px 0px #111" }}>
            <h2 className="text-3xl font-black mb-2" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>Project Not Found</h2>
            <p className="text-sm mb-4" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>The project you're looking for doesn't exist.</p>
            <Link
              to="/dashboard"
              className="inline-block font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black"
              style={{ background: "#ADFF2F", boxShadow: "4px 4px 0px #111", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8" style={{ background: "#F4EFE4" }}>
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Button */}
        <div className="mb-6">
          <Link
            to="/dashboard"
            className="inline-flex items-center font-black text-sm uppercase tracking-widest"
            style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M15 19l-7-7 7-7" />
            </svg>
            Back to Dashboard
          </Link>
        </div>

        {/* Page Header */}
        <div className="bg-white rounded-lg border-2 border-black p-6 mb-6" style={{ boxShadow: "8px 8px 0px #111" }}>
          <h1 className="text-4xl font-black mb-2" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>
            {project.Title || 'Renovation Project Details'}
          </h1>
          {project.City && (
            <p className="text-lg font-bold mb-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
              📍 {project.City}
            </p>
          )}
          {project.$createdAt && (
            <p className="text-sm" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
              Created on {new Date(project.$createdAt).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </p>
          )}
        </div>

        {/* Project Images */}
        <div className="bg-white rounded-lg border-2 border-black p-6 mb-6" style={{ boxShadow: "8px 8px 0px #111" }}>
          <h2 className="text-2xl font-black mb-4" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>Project Images</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Current Photo */}
            <div>
              <h3 className="text-sm font-black uppercase tracking-widest mb-3" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Current State
              </h3>
              {project.CurrentPhoto ? (
                <div className="relative">
                  <img
                    src={getImageUrl(project.CurrentPhoto)}
                    alt="Current state of the space"
                    className="w-full h-auto rounded-lg border-2 border-black"
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect fill="%23e5e7eb" width="400" height="300"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%236b7280" font-size="20">Image not available</text></svg>';
                    }}
                  />
                </div>
              ) : (
                <div className="w-full h-64 bg-white rounded-lg flex items-center justify-center border-2 border-black">
                  <span className="text-xs font-black uppercase" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>No current photo available</span>
                </div>
              )}
            </div>

            {/* Final/Ideal Photo */}
            <div>
              <h3 className="text-sm font-black uppercase tracking-widest mb-3" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Final Result
              </h3>
              {project.Idealphoto ? (
                <div className="relative">
                  <img
                    src={getImageUrl(project.Idealphoto)}
                    alt="Final result of the renovation"
                    className="w-full h-auto rounded-lg border-2 border-black"
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect fill="%23e5e7eb" width="400" height="300"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%236b7280" font-size="20">Image not available</text></svg>';
                    }}
                  />
                </div>
              ) : (
                <div className="w-full h-64 bg-white rounded-lg flex items-center justify-center border-2 border-black">
                  <span className="text-xs font-black uppercase" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>No final photo available</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Project Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Budget */}
          <div className="bg-white rounded-lg border-2 border-black p-6" style={{ boxShadow: "8px 8px 0px #111" }}>
            <div className="flex items-center mb-3">
              <svg
                className="w-6 h-6 mr-2"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
                style={{ color: "#111" }}
              >
                <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-sm font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>Budget</h3>
            </div>
            <p className="text-4xl font-black" style={{ fontFamily: "'Lilita One', Arial, sans-serif", color: "#111" }}>
              ₹{project.Budget?.toLocaleString() || 'N/A'}
            </p>
          </div>

          {/* Project Info */}
          <div className="bg-white rounded-lg border-2 border-black p-6" style={{ boxShadow: "8px 8px 0px #111" }}>
            <div className="flex items-center mb-3">
              <svg
                className="w-6 h-6 mr-2"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
                style={{ color: "#111" }}
              >
                <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-sm font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>Project Information</h3>
            </div>
            <div className="space-y-2">
              <div>
                <span className="text-xs font-black uppercase" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>Project Name:</span>
                <p className="text-sm break-all" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>{project.Title || 'Untitled Project'}</p>
              </div>
              {project.$updatedAt && (
                <div>
                  <span className="text-xs font-black uppercase" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>Last Updated:</span>
                  <p className="text-sm" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                    {new Date(project.$updatedAt).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="bg-white rounded-lg border-2 border-black p-6 mb-6" style={{ boxShadow: "8px 8px 0px #111" }}>
          <div className="flex items-center mb-3">
            <svg
              className="w-6 h-6 mr-2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
              style={{ color: "#111" }}
            >
              <path d="M4 6h16M4 12h16M4 18h7" />
            </svg>
            <h3 className="text-sm font-black uppercase tracking-widest" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>Project Description</h3>
          </div>
          <p className="leading-relaxed whitespace-pre-wrap" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#333", fontSize: "14px" }}>
            {project.Description || 'No description provided for this project.'}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <Link
            to="/dashboard"
            className="font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black transition-all"
            style={{ background: "transparent", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
          >
            Back to Projects
          </Link>
          <Link
            to="/upload"
            className="font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black transition-all"
            style={{ background: "#ADFF2F", boxShadow: "4px 4px 0px #111", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
          >
            Start New Project
          </Link>
        </div>
      </div>
    </div>
  );
};

export default EachOldProject;