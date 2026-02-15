import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav
      className="navbar"
      style={{
        backgroundColor: "#4f46e5",
        padding: "12px 20px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        color: "white"
      }}
    >
      <div className="logo" style={{ fontWeight: "bold", fontSize: "18px" }}>
        🌍 Travel Genie
      </div>

      <div className="nav-links" style={{ display: "flex", gap: "16px", alignItems: "center" }}>
        <Link to="/" style={{ color: "white", textDecoration: "none" }}>
          Home
        </Link>

        {user ? (
          <>
            <Link to="/chat" style={{ color: "white", textDecoration: "none" }}>
              Chat
            </Link>
            <Link to="/itineraries" style={{ color: "white", textDecoration: "none" }}>
              Itineraries
            </Link>
            <button
              onClick={logout}
              style={{
                backgroundColor: "white",
                color: "#4f46e5",
                border: "none",
                padding: "6px 12px",
                borderRadius: "6px"
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: "white", textDecoration: "none" }}>
              Login
            </Link>
            <Link to="/signup" style={{ color: "white", textDecoration: "none" }}>
              Signup
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
