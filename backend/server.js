// server.js
import express from "express";
import cors from "cors";
import { PythonShell } from "python-shell";
import OpenAI from "openai";
import path from "path";
import { fileURLToPath } from "url";
import "dotenv/config";

const app = express();
app.use(cors());
app.use(express.json());

// ✅ OpenAI client
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// ✅ Path setup
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PYTHON_PATH =
  "C:\\Users\\sudheer\\AppData\\Local\\Programs\\Python\\Python310\\python.exe";

// ✅ CHAT ROUTE
app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  console.log("\n📩 User Sent:", userMessage);

  let memoryReply = null;

  try {
    const output = await PythonShell.run("chat_api.py", {
      pythonPath: PYTHON_PATH,
      scriptPath: path.join(__dirname, "../src"),
      args: [userMessage],
    });

    try {
      memoryReply = JSON.parse(output?.[0]).reply;
    } catch {
      memoryReply = output?.[0];
    }
  } catch (err) {
    console.error("❌ Python Error:", err);
  }

  const context = memoryReply ? `User memory: ${memoryReply}` : "";

  const gptResponse = await client.chat.completions.create({
    model: "gpt-4.1-mini",
    messages: [
      {
        role: "system",
        content: `
You reply in **maximum 6 words**.
Use memory if it's relevant.`,
      },
      { role: "user", content: `${context}\nUser: ${userMessage}` },
    ],
  });

  const finalReply = gptResponse.choices[0].message.content
    .split(" ")
    .slice(0, 6)
    .join(" ");

  return res.json({
    reply: finalReply,
    memory: memoryReply,
  });
});

// ✅ LIST MEMORIES
app.get("/memory/list", async (req, res) => {
  try {
    const output = await PythonShell.run("memory_api.py", {
      pythonPath: PYTHON_PATH,
      scriptPath: path.join(__dirname, "../src"),
    });

    return res.json({ memories: JSON.parse(output[0]) });
  } catch (error) {
    console.error("❌ Error listing memories:", error);
    return res.json({ memories: [] });
  }
});

// ✅ DELETE MEMORY
app.post("/memory/delete", async (req, res) => {
  const { id } = req.body;

  try {
    await PythonShell.run("delete_api.py", {
      pythonPath: PYTHON_PATH,
      scriptPath: path.join(__dirname, "../src"),
      args: [id],
    });

    return res.json({ success: true });
  } catch (error) {
    console.error("❌ Delete error:", error);
    return res.json({ success: false });
  }
});

// ✅ START SERVER
app.listen(5000, () =>
  console.log("✅ Backend running → http://localhost:5000")
);
