import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    login(email, password);
    navigate("/chat");
  };

  return (
    <div className="auth-bg">
      <div className="auth-card">
        <h1>Welcome Back</h1>
        <p>Login to continue your journey ✈️</p>

        <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogin}>Login</button>

        <div className="auth-footer">
          <span>Don’t have an account?</span>
          <Link to="/signup">Create one</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;