// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Upload Page – Old & New Room Images
// ============================================

import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import service from "../../appwrite/service";
import renovationAPI from "../../api/renovation";
import { logger } from "../../Conf/conf";

const Upload = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState("");
  const [currentPhotoPreview, setCurrentPhotoPreview] = useState(null);
  const [idealPhotoPreview, setIdealPhotoPreview] = useState(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
    trigger,
  } = useForm();

  const currentPhotoFile = watch("currentPhoto");
  const idealPhotoFile = watch("idealPhoto");

  // Preview images when selected
  React.useEffect(() => {
    if (currentPhotoFile && currentPhotoFile[0]) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCurrentPhotoPreview(reader.result);
      };
      reader.readAsDataURL(currentPhotoFile[0]);
    }
  }, [currentPhotoFile]);

  React.useEffect(() => {
    if (idealPhotoFile && idealPhotoFile[0]) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setIdealPhotoPreview(reader.result);
      };
      reader.readAsDataURL(idealPhotoFile[0]);
    }
  }, [idealPhotoFile]);

  const handleAnalyze = async () => {
    // Validate required fields before analyzing
    const isCurrentPhotoValid = await trigger("currentPhoto");
    const isIdealPhotoValid = await trigger("idealPhoto");

    if (!isCurrentPhotoValid || !isIdealPhotoValid) {
      setError("Please upload both current and ideal photos before analyzing");
      return;
    }

    setError("");
    setAnalyzing(true);

    try {
      // Get current form values
      const currentPhoto = watch("currentPhoto")[0];
      const idealPhoto = watch("idealPhoto")[0];
      const budget = watch("budget");
      const city = watch("city");
      const title = watch("title");
      
      // Call backend API to analyze images
      const analysisResult = await renovationAPI.analyzeRenovation({
        currentImage: currentPhoto,
        idealImage: idealPhoto,
        budget: budget ? parseFloat(budget) : null,
        city: city || null,
        title: title || null,
      });
      
      // Build comprehensive description with plan details
      let fullDescription = analysisResult.explanation || "Analysis complete.";
      
      // Add plan details if available
      if (analysisResult.plan && analysisResult.plan.length > 0) {
        fullDescription += "\n\n📋 DETAILED RENOVATION PLAN:\n\n";
        
        let planTotal = 0;
        analysisResult.plan.forEach((item, index) => {
          const priorityEmoji = 
            item.priority === 'high' ? '🔴' : 
            item.priority === 'medium' ? '🟡' : '🟢';
          
          fullDescription += `${index + 1}. ${item.task.toUpperCase()} ${priorityEmoji}\n`;
          fullDescription += `   Priority: ${item.priority.charAt(0).toUpperCase() + item.priority.slice(1)}\n`;
          fullDescription += `   Cost: ₹${Math.round(item.cost).toLocaleString()}\n`;
          fullDescription += `   Details: ${item.description}\n\n`;
          
          planTotal += item.cost;
        });
        
        // Add summary with verification
        fullDescription += `\n💰 COST SUMMARY:\n`;
        fullDescription += `Individual Tasks Total: ₹${Math.round(planTotal).toLocaleString()}\n`;
        fullDescription += `Total Estimated Cost: ₹${Math.round(analysisResult.estimated_cost).toLocaleString()}\n`;
        fullDescription += `Currency: ${analysisResult.currency}\n`;
        
        if (analysisResult.optimized) {
          fullDescription += `✅ This plan has been optimized to fit your budget!\n`;
        }
        
        fullDescription += `\n📊 Overall Condition Score: ${(analysisResult.score * 100).toFixed(1)}%\n`;
        fullDescription += `(Higher score indicates more renovation work needed)`;
      }
      
      // Auto-fill the description field with comprehensive analysis
      setValue("description", fullDescription);
      
      // Store analysis result for later use (budget auto-fill)
      setAnalysisResult(analysisResult);
      setAnalyzed(true);
      
      // Log for debugging (dev only)
      logger.log("Analysis complete:", {
        score: analysisResult.score,
        estimatedCost: analysisResult.estimated_cost,
        optimized: analysisResult.optimized,
        plan: analysisResult.plan,
      });
      
    } catch (error) {
      logger.error("Analysis error:", error);
      setError(error.message || "Failed to analyze. Please try again.");
    } finally {
      setAnalyzing(false);
    }
  };

  const onSubmit = async (data) => {
    if (!user) {
      setError("Please login to upload a project");
      navigate("/login");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // Step 1: Upload Current Photo to storage
      const currentPhotoUpload = await service.uploadImage(data.currentPhoto[0]);
      if (!currentPhotoUpload) {
        throw new Error("Failed to upload current photo");
      }

      // Step 2: Upload Ideal Photo to storage
      const idealPhotoUpload = await service.uploadImage(data.idealPhoto[0]);
      if (!idealPhotoUpload) {
        throw new Error("Failed to upload ideal photo");
      }

      // Step 3: Create database row with file IDs
      // Use user-provided budget, or if not provided, use backend estimated cost
      const finalBudget = data.budget 
        ? parseInt(data.budget) 
        : (analysisResult?.estimated_cost ? Math.round(analysisResult.estimated_cost) : null);
      
      const projectData = {
        title: data.title,
        city: data.city,
        currentImage: currentPhotoUpload.$id,
        idealImage: idealPhotoUpload.$id,
        budget: finalBudget,
        description: data.description,
        userId: user.$id, // Add current user's ID
      };

      const newProject = await service.createRow(projectData);

      if (newProject) {
        // Success! Navigate to dashboard
        navigate("/dashboard");
      } else {
        throw new Error("Failed to create project");
      }
    } catch (error) {
      logger.error("Upload error:", error);
      setError(error.message || "Failed to upload project. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Redirect to login if not authenticated
  if (!user) {
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
        `}</style>
        
        <div className="flex items-center justify-center min-h-screen" style={{ background: "#F4EFE4" }}>
          <div className="text-center max-w-md mx-auto p-8 bg-white border-2 border-black rounded-2xl" style={{ boxShadow: "8px 8px 0px #111" }}>
            <h2 className="form-title text-4xl mb-2">LOGIN REQUIRED</h2>
            <p className="text-sm font-semibold mb-6" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
              Please login to upload a renovation project.
            </p>
            <button
              onClick={() => navigate("/login")}
              className="font-black text-sm uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black"
              style={{
                background: "#ADFF2F",
                boxShadow: "4px 4px 0px #111",
                fontFamily: "'Boogaloo', Arial, sans-serif",
                color: "#111"
              }}
            >
              GO TO LOGIN →
            </button>
          </div>
        </div>
      </>
    );
  }
  
  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Lilita+One&display=swap');
        .page-header {
          font-family: 'Lilita One', 'Arial Black', sans-serif;
          -webkit-text-stroke: 2.5px #111;
          color: transparent;
          paint-order: stroke fill;
          letter-spacing: -1px;
        }
      `}</style>
      
      <div className="min-h-screen py-8" style={{ background: "#F4EFE4" }}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="page-header text-5xl mb-2" style={{ lineHeight: "1.1" }}>
              NEW PROJECT
            </h1>
            <p className="text-sm font-bold uppercase" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", letterSpacing: "0.06em", color: "#555" }}>
              Upload your current and ideal room images
            </p>
          </div>

        {/* Error Message */}
        {error && (
          <div className="font-bold uppercase tracking-wide text-sm px-4 py-3 rounded-lg mb-6 border-2 border-red-500 bg-red-50 text-red-700">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-8 border-2 border-black rounded-2xl" style={{ boxShadow: "8px 8px 0px #111" }}>
          <div className="space-y-6">
            {/* Title Field */}
            <div>
              <label htmlFor="title" className="block text-xs font-black uppercase tracking-widest mb-2" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Project Title <span className="text-red-600">*</span>
              </label>
              <input
                id="title"
                type="text"
                placeholder="e.g., Living Room Renovation"
                {...register("title", {
                  required: "Project title is required",
                })}
                className="w-full px-3 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
              {errors.title && (
                <p className="text-red-600 text-xs mt-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif" }}>{errors.title.message}</p>
              )}
            </div>

            {/* City Field */}
            <div>
              <label htmlFor="city" className="block text-xs font-black uppercase tracking-widest mb-2" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                City <span className="text-red-600">*</span>
              </label>
              <input
                id="city"
                type="text"
                placeholder="e.g., New York"
                {...register("city", {
                  required: "City is required",
                })}
                className="w-full px-3 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
              {errors.city && (
                <p className="text-red-600 text-xs mt-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif" }}>{errors.city.message}</p>
              )}
            </div>

            {/* Current Photo Upload */}
            <div>
              <label htmlFor="currentPhoto" className="block text-xs font-black uppercase tracking-widest mb-2" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Current Photo <span className="text-red-600">*</span>
              </label>
              <div className="flex flex-col space-y-3">
                <input
                  id="currentPhoto"
                  type="file"
                  accept="image/*"
                  {...register("currentPhoto", {
                    required: "Current photo is required",
                  })}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                {errors.currentPhoto && (
                  <p className="text-red-600 text-sm">{errors.currentPhoto.message}</p>
                )}
                {currentPhotoPreview && (
                  <div className="mt-3">
                    <img
                      src={currentPhotoPreview}
                      alt="Current room preview"
                      className="max-w-full h-auto max-h-64 rounded-lg border border-gray-300"
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Ideal Photo Upload */}
            <div>
              <label htmlFor="idealPhoto" className="block text-xs font-black uppercase tracking-widest mb-2" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Ideal Photo <span className="text-red-600">*</span>
              </label>
              <div className="flex flex-col space-y-3">
                <input
                  id="idealPhoto"
                  type="file"
                  accept="image/*"
                  {...register("idealPhoto", {
                    required: "Ideal photo is required",
                  })}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                {errors.idealPhoto && (
                  <p className="text-red-600 text-sm">{errors.idealPhoto.message}</p>
                )}
                {idealPhotoPreview && (
                  <div className="mt-3">
                    <img
                      src={idealPhotoPreview}
                      alt="Ideal room preview"
                      className="max-w-full h-auto max-h-64 rounded-lg border border-gray-300"
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Budget Field */}
            <div>
              <label htmlFor="budget" className="block text-xs font-black uppercase tracking-widest mb-2" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                Budget (Optional)
              </label>
              <input
                id="budget"
                type="number"
                placeholder="Enter budget amount (minimum 15,000)"
                {...register("budget", {
                  min: {
                    value: 15000,
                    message: "Budget must be at least 15,000",
                  },
                })}
                className="w-full px-3 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                disabled={analyzed}
              />
              {errors.budget && (
                <p className="text-red-600 text-xs mt-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif" }}>{errors.budget.message}</p>
              )}
              <p className="text-xs mt-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>Minimum budget is ₹15,000</p>
            </div>

            {/* Analyze Button */}
            {!analyzed && (
              <div className="pt-2">
                <button
                  type="button"
                  onClick={handleAnalyze}
                  disabled={analyzing}
                  className="w-full font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{ background: "#ADFF2F", boxShadow: "4px 4px 0px #111", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
                >
                  {analyzing ? (
                    <span className="flex items-center justify-center">
                      <svg
                        className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      Analyzing...
                    </span>
                  ) : (
                    "Analyze & Generate Description"
                  )}
                </button>
                <p className="text-xs mt-2 text-center" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
                  Click to analyze your images and generate a project description
                </p>
              </div>
            )}

            {/* Description Field - Only shown after analysis */}
            {analyzed && (
              <div>
                <label htmlFor="description" className="block text-xs font-black uppercase tracking-widest mb-2" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}>
                  Generated Project Description
                </label>
                <textarea
                  id="description"
                  rows="18"
                  {...register("description", {
                    required: "Description is required",
                  })}
                  readOnly
                  className="w-full px-3 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 bg-gray-50 font-mono text-sm cursor-default"
                  style={{ whiteSpace: "pre-wrap" }}
                />
                {errors.description && (
                  <p className="text-red-600 text-xs mt-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif" }}>{errors.description.message}</p>
                )}
                <p className="text-xs mt-1" style={{ fontFamily: "'Boogaloo', Arial, sans-serif", color: "#555" }}>
                  This description was generated based on your images and budget analysis.
                </p>
              </div>
            )}

            {/* Submit Buttons - Only shown after analysis */}
            {analyzed && (
              <div className="flex gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setAnalyzed(false);
                    setAnalysisResult(null);
                    setValue("description", "");
                  }}
                  className="flex-1 font-black text-base uppercase tracking-widest px-6 py-3 rounded-full border-2 border-black transition-all"
                  style={{ background: "transparent", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
                >
                  Re-analyze
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 font-black text-base uppercase tracking-widest px-6 py-3 rounded-full border-2 border-black transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{ background: "#ADFF2F", boxShadow: "4px 4px 0px #111", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg
                        className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      Uploading...
                    </span>
                  ) : (
                    "Create Project"
                  )}
                </button>
              </div>
            )}

            {/* Cancel Button - Always shown before analysis */}
            {!analyzed && (
              <div className="pt-4">
                <button
                  type="button"
                  onClick={() => navigate("/dashboard")}
                  className="w-full font-black text-base uppercase tracking-widest px-8 py-3 rounded-full border-2 border-black transition-all"
                  style={{ background: "transparent", fontFamily: "'Boogaloo', Arial, sans-serif", color: "#111" }}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>
        </form>
      </div>
    </div>
    </>
  );
};

export default Upload;