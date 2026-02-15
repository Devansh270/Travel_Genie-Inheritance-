import express from "express";
import cors from "cors";
import fetch from "node-fetch";

const app = express();

app.use(cors());
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error connecting to Python:", error);
    res.status(500).json({ error: "Backend error" });
  }
});

app.listen(5000, () => {
  console.log("Node server running on http://localhost:5000");
});
