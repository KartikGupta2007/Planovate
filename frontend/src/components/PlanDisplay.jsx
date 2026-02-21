// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Plan Display – Shows Step-by-Step Plan
// ============================================

import React from "react";

const PlanDisplay = ({ plan, explanation }) => {
  // plan = [{ task, priority, cost, description }]
  // explanation = string from LLM

  return (
    <div className="plan-display">
      <h3>Renovation Plan</h3>

      {explanation && (
        <div className="explanation">
          <p>{explanation}</p>
        </div>
      )}

      {/* TODO: Render each plan step */}
      {plan && plan.map((step, index) => (
        <div key={index} className="plan-step">
          <h4>Step {index + 1}: {step.task}</h4>
          <p>Priority: {step.priority}</p>
          <p>Estimated Cost: ${step.cost}</p>
          <p>{step.description}</p>
        </div>
      ))}
    </div>
  );
};

export default PlanDisplay;
