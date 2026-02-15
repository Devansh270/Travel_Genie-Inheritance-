import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = () => {
    signup(email, password);
    navigate("/chat");
  };

  return (
    <div className="auth-bg">
      <div className="auth-card">
        <h1>Create Account</h1>
        <p>Start planning your journeys 🌍</p>

        <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleSignup}>Sign Up</button>

        <div className="auth-footer">
          <span>Already have an account?</span>
          <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
}

export default Signup;