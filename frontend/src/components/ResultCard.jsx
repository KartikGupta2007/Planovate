// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Result Card – Displays Renovation Score
// ============================================

import React from "react";

const ResultCard = ({ score }) => {
  // TODO: Add visual score indicator (progress bar, color coding, etc.)

  return (
    <div className="result-card">
      <h3>Renovation Score</h3>
      <p className="score">{(score * 100).toFixed(1)}%</p>
    </div>
  );
};

export default ResultCard;
