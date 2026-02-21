// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: History Page – Past Renovation Projects
// ============================================

import React, { useEffect, useState } from "react";
// TODO: import { getUserHistory } from "../api/renovation";

const History = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch user's past projects
    // const data = await getUserHistory(userId);
    // setProjects(data);
    setLoading(false);
  }, []);

  return (
    <div className="history-page">
      <h2>My Renovation History</h2>

      {loading && <p>Loading...</p>}

      {!loading && projects.length === 0 && (
        <p>No past projects found. Start a new renovation!</p>
      )}

      {/* TODO: Map over projects and display summary cards */}
      {projects.map((project, index) => (
        <div key={index} className="history-card">
          <p>Score: {project.score}</p>
          <p>Cost: {project.estimated_cost}</p>
        </div>
      ))}
    </div>
  );
};

export default History;
