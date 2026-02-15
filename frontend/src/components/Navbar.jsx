import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="logo">🌍 Travel Genie</div>

      <div className="nav-links">
        <Link to="/">Home</Link>

        {user ? (
          <>
            <Link to="/chat">Chat</Link>
            <Link to="/itineraries">Itineraries</Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;