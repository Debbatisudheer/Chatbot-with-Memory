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

// ✅ Proper Python path
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PYTHON_PATH =
  "C:\\Users\\sudheer\\AppData\\Local\\Programs\\Python\\Python310\\python.exe";

// ✅ Home test route
app.get("/", (req, res) => {
  res.send("✅ Backend working! POST /chat to talk to chatbot.");
});

// ✅ CHAT API
app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  console.log("📩 UI Sent:", userMessage);

  let memoryReply = null;

  try {
    const output = await PythonShell.run("chat_api.py", {
      pythonPath: PYTHON_PATH,
      mode: "text",
      scriptPath: path.join(__dirname, "../src"),
      args: [userMessage],
    });

    memoryReply = output[0]?.trim();     // ✅ always string
    console.log("🧠 Memory Reply (Python):", memoryReply);

  } catch (err) {
    console.error("❌ Python Error:", err);
  }

  // ✅ Build memory context to supply to GPT
  const memoryContext =
    memoryReply && memoryReply !== "Interesting... tell me more."
      ? `User memory: ${memoryReply}`
      : "No memory available.";

  // ✅ Send request to GPT with memory context
  try {
    const gptResponse = await client.chat.completions.create({
      model: "gpt-4.1-mini",
      messages: [
        {
          role: "system",
          content: `
You are a memory-enhanced chatbot.
Use the stored memory when the user asks related questions.

Memory:
${memoryContext}

Rules:
- If memory is relevant, answer from memory.
- If user asks "who is my favorite god" and memory includes "love Shiva", infer the answer.
- Never say "I don't know" if memory exists.
          `,
        },
        { role: "user", content: userMessage },
      ],
    });

    const reply = gptResponse.choices[0].message.content;
    console.log("🤖 GPT Reply:", reply);

    return res.json({ reply });

  } catch (err) {
    console.error("❌ GPT Error:", err);
    return res.json({ reply: "⚠️ GPT Error" });
  }
});

// ✅ Start server
app.listen(5000, () =>
  console.log("✅ Backend running on http://localhost:5000")
);
