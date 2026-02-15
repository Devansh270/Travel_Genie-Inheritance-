import React, { useEffect, useState } from "react";

function Itineraries() {
  const [trips, setTrips] = useState([]);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("itineraries")) || [];
    setTrips(saved);
  }, []);

  return (
    <div className="itinerary-page">
      <h2>Your Itineraries</h2>

      {trips.length === 0 && <p>No trips saved yet.</p>}

      <div className="itinerary-grid">
        {trips.map((trip, i) => (
          <div key={i} className="itinerary-card">
            <h3>{trip.title}</h3>
            <p>Saved Trip</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Itineraries;