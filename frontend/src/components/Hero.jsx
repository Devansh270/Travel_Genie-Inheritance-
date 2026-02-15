import React from "react";
import { useNavigate } from "react-router-dom";

function Hero() {
  const navigate = useNavigate();

  return (
    <section className="hero">
      <h1>Plan Smarter. Travel Better.</h1>
      <p>Your AI-powered travel companion</p>
      <button onClick={() => navigate("/planner")}>Start Planning</button>
    </section>
  );
}

export default Hero;