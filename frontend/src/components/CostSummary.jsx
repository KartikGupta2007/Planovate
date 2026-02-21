// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Cost Summary Component
// ============================================

import React from "react";

const CostSummary = ({ estimatedCost, optimized, budget }) => {
  return (
    <div className="cost-summary">
      <h3>Cost Summary</h3>
      <p>Estimated Total: <strong>${estimatedCost?.toLocaleString()}</strong></p>
      {budget && <p>Your Budget: <strong>${Number(budget).toLocaleString()}</strong></p>}
      {optimized && <p className="optimized-badge">Plan optimized for your budget</p>}
    </div>
  );
};

export default CostSummary;
