import React, { useState } from "react";
import axios from "axios";
import ChatBox from "../components/ChatBox";

function Chat() {
  const [chat, setChat] = useState([]);
  const [lastTrip, setLastTrip] = useState(null);

  const handleSend = async (msg) => {
    try {
      // Add user message immediately
      setChat((prev) => [...prev, { from: "user", text: msg }]);

      // Call Node backend (IMPORTANT: /api/chat)
      const response = await axios.post("http://localhost:5000/api/chat", {
        query: msg,
      });

      const botReply = response.data.itinerary || "No itinerary generated.";

      setChat((prev) => [
        ...prev,
        { from: "bot", text: botReply },
      ]);

      setLastTrip({
        title: msg,
        createdAt: new Date().toISOString(),
      });

    } catch (error) {
      console.error("Chat error:", error);
      setChat((prev) => [
        ...prev,
        { from: "bot", text: "⚠️ Something went wrong." },
      ]);
    }
  };

  const addToItinerary = () => {
    if (!lastTrip) return;

    const existing = JSON.parse(localStorage.getItem("itineraries")) || [];
    existing.push(lastTrip);
    localStorage.setItem("itineraries", JSON.stringify(existing));
    alert("Trip added to itineraries ✅");
  };

  return (
    <div className="chat-page">
      <div className="chat-window">
        {chat.map((c, i) => (
          <div key={i} className={c.from === "user" ? "chat user" : "chat bot"}>
            {c.text}
          </div>
        ))}

        {lastTrip && (
          <div style={{ textAlign: "center", margin: "20px 0" }}>
            <button className="add-btn" onClick={addToItinerary}>
              ➕ Add to Itinerary
            </button>
          </div>
        )}
      </div>

      <ChatBox onSend={handleSend} />
    </div>
  );
}

export default Chat;
