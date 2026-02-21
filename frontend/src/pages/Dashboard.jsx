// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Dashboard – Shows Renovation Results
// ============================================

import React from "react";
// TODO: import { useLocation } from "react-router-dom";
// TODO: import ResultCard from "../components/ResultCard";
// TODO: import PlanDisplay from "../components/PlanDisplay";
// TODO: import CostSummary from "../components/CostSummary";

const Dashboard = () => {
  // TODO: const { state } = useLocation();
  // TODO: const result = state?.result;

  // Placeholder result shape (matches API contract):
  // {
  //   score: 0.65,
  //   estimated_cost: 72000,
  //   optimized: true,
  //   plan: [...],
  //   explanation: "..."
  // }

  return (
    <div className="dashboard-page">
      <h2>Renovation Plan Results</h2>

      {/* TODO: Show result data using components */}
      {/* <ResultCard score={result.score} /> */}
      {/* <CostSummary estimatedCost={result.estimated_cost} optimized={result.optimized} /> */}
      {/* <PlanDisplay plan={result.plan} explanation={result.explanation} /> */}

      <p>Results will appear here after analysis.</p>
    </div>
  );
};

export default Dashboard;
