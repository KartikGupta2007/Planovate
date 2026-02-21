// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Image Uploader Component
// ============================================

import React, { useState } from "react";

const ImageUploader = ({ label, onImageSelect }) => {
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onImageSelect(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  return (
    <div className="image-uploader">
      <label>{label}</label>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {preview && <img src={preview} alt="Preview" className="image-preview" />}
    </div>
  );
};

export default ImageUploader;
