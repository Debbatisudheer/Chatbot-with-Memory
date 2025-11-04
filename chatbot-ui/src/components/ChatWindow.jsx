import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../lib/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello 👋 I remember what you tell me!" },
  ]);
  const [input, setInput] = useState("");
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    if (!input.trim()) return;

    const userText = input;
    setMessages((prev) => [...prev, { from: "user", text: userText }]);
    setInput("");

    const res = await sendMessage(userText);
    setMessages((prev) => [...prev, { from: "bot", text: res.reply }]);
  }

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      <div className="p-4 font-bold bg-gray-800 border-b border-gray-700">
        Memory Chatbot 💬
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg max-w-[70%] ${
              msg.from === "user"
                ? "bg-green-600 ml-auto"
                : "bg-gray-700 mr-auto"
            }`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={bottomRef}></div>
      </div>

      <div className="p-3 border-t border-gray-800 flex gap-2">
        <input
          className="flex-1 p-3 rounded bg-gray-800 outline-none"
          placeholder="Type something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="bg-green-600 px-4 py-3 rounded" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

