import React from "react";
import { useNavigate } from "react-router-dom";

function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <h1>🌍 Travel Genie</h1>
      <p>Your AI Travel Assistant</p>
      <button onClick={() => navigate("/login")}>Start</button>
    </div>
  );
}

export default Landing;