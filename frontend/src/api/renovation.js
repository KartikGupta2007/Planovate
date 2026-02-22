// ============================================
// OWNER: Member 1 – Frontend + Backend API Integration
// FILE: Renovation API Service
// ============================================

import conf from "../Conf/conf";
``
const BASE_URL = "https://planovate-production-dc6d.up.railway.app";

class RenovationAPI {
  constructor() {
    this.baseURL = BASE_URL || conf.backendApiUrl;
  }

  /**
   * Analyze renovation images and generate description
   * @param {Object} params - Analysis parameters
   * @param {File} params.currentImage - Current room image file
   * @param {File} params.idealImage - Ideal room image file
   * @param {number} params.budget - Budget in INR (optional)
   * @param {string} params.city - City/location (optional)
   * @param {string} params.title - Project title (optional)
   * @returns {Promise<Object>} - Analysis result with description
   */
  async analyzeRenovation({ currentImage, idealImage, budget, city, title }) {
    try {
      const formData = new FormData();
      
      // Required fields
      formData.append('old_image', currentImage);
      formData.append('new_image', idealImage);
      
      // Optional fields
      if (budget) {
        formData.append('budget', budget.toString());
      }
      if (city) {
        formData.append('location', city);
      }

      const response = await fetch(`${this.baseURL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Backend returns:
      // {
      //   score: 0.65,
      //   estimated_cost: 72000,
      //   optimized: true,
      //   currency: "INR",
      //   plan: [...],
      //   explanation: "Based on the analysis..."
      // }
      
      return data;
    } catch (error) {
      console.error('Renovation analysis error:', error);
      throw error;
    }
  }

  /**
   * Health check for backend API
   * @returns {Promise<Object>}
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/api/health`);
      return await response.json();
    } catch (error) {
      console.error('Backend health check failed:', error);
      throw error;
    }
  }
}

const renovationAPI = new RenovationAPI();
export default renovationAPI;
