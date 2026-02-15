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
    <div className="chatbox">
      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask Travel Genie..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default ChatBox;
