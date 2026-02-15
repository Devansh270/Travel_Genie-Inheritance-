import React, { useState } from "react";

function ChatBox({ onSend }) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  };

  return (
    <div className="chatbox" style={{ backgroundColor: "#f5f7fb", padding: "10px" }}>
      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask Travel Genie..."
          style={{
            border: "2px solid #4f46e5",
            borderRadius: "8px",
            padding: "8px",
            marginRight: "8px"
          }}
        />
        <button
          type="submit"
          style={{
            backgroundColor: "#4f46e5",
            color: "white",
            border: "none",
            borderRadius: "8px",
            padding: "8px 14px"
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatBox;
