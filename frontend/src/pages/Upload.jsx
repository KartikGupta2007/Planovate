// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Upload Page – Old & New Room Images
// ============================================

import React, { useState } from "react";
// TODO: import ImageUploader from "../components/ImageUploader";
// TODO: import { analyzeRenovation } from "../api/renovation";
// TODO: import { useNavigate } from "react-router-dom";

const Upload = () => {
  const [oldImage, setOldImage] = useState(null);
  const [newImage, setNewImage] = useState(null);
  const [budget, setBudget] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!oldImage || !newImage) return;

    setLoading(true);
    // TODO: Upload images to Appwrite storage
    // TODO: Call backend API with image URLs and budget
    // const result = await analyzeRenovation(oldImageUrl, newImageUrl, budget);
    // navigate("/dashboard", { state: { result } });
    setLoading(false);
  };

  return (
    <div className="upload-page">
      <h2>Upload Room Images</h2>
      <form onSubmit={handleSubmit}>
        <div className="image-section">
          <label>Current Room (Old)</label>
          {/* TODO: Replace with <ImageUploader onImageSelect={setOldImage} /> */}
          <input type="file" accept="image/*" onChange={(e) => setOldImage(e.target.files[0])} />
        </div>

        <div className="image-section">
          <label>Ideal Room (New)</label>
          {/* TODO: Replace with <ImageUploader onImageSelect={setNewImage} /> */}
          <input type="file" accept="image/*" onChange={(e) => setNewImage(e.target.files[0])} />
        </div>

        <div className="budget-section">
          <label>Budget (Optional)</label>
          <input
            type="number"
            placeholder="Enter budget amount"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Generate Renovation Plan"}
        </button>
      </form>
    </div>
  );
};

export default Upload;
