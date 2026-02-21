// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: API Service – Calls to Backend
// ============================================

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Send images to backend for renovation analysis
 * Matches API Contract:
 *   Request:  { old_image, new_image, budget }
 *   Response: { score, estimated_cost, optimized, plan, explanation }
 */
export const analyzeRenovation = async (oldImageUrl, newImageUrl, budget = null) => {
  // TODO: Implement actual API call
  // const response = await fetch(`${API_BASE}/api/analyze`, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({
  //     old_image: oldImageUrl,
  //     new_image: newImageUrl,
  //     budget: budget ? Number(budget) : null,
  //   }),
  // });
  // return await response.json();
  return null;
};

/**
 * Fetch user's renovation history
 */
export const getUserHistory = async (userId) => {
  // TODO: Implement actual API call
  // const response = await fetch(`${API_BASE}/api/history/${userId}`);
  // return await response.json();
  return [];
};
