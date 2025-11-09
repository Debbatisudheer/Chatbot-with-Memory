// ---------------- MemoryPanel.jsx ----------------
import { useEffect, useState } from "react";
import axios from "axios";

export default function MemoryPanel() {
  const [memories, setMemories] = useState([]);

  async function loadMemories() {
    try {
      const res = await axios.get("http://localhost:5000/memory/list");

      if (!Array.isArray(res.data.memories)) {
        console.error("Unexpected memory data format:", res.data);
        return;
      }

      setMemories(res.data.memories); // ✅ direct array
    } catch (err) {
      console.error("Error loading memories:", err);
    }
  }

  async function handleDelete(id) {
    try {
      await axios.delete(`http://localhost:5000/memory/delete/${id}`);
      loadMemories(); // ✅ refresh UI
    } catch (err) {
      console.error("Delete failed:", err);
    }
  }

  useEffect(() => {
    loadMemories();
  }, []);

  return (
    <div className="w-full bg-gray-100 p-4 border-l overflow-y-auto">
      <h2 className="text-lg font-bold mb-3">🧠 Stored Memories</h2>

      {memories.length === 0 && (
        <p className="text-gray-500">No memories stored yet.</p>
      )}

      {memories.map((m) => {
        const type = m.metadata?.type?.toUpperCase() || "UNKNOWN";
        const value = m.metadata?.value || "(empty)";
        const id = m.id; // ✅ Always use Pinecone vector ID

        return (
          <div
            key={id}
            className="flex justify-between bg-white p-3 rounded mb-2 shadow"
          >
            <div>
              <strong className="text-blue-600">{type}</strong> — {value}
            </div>

            <button
              onClick={() => handleDelete(id)}
              className="bg-red-500 px-3 py-1 text-xs text-white rounded hover:bg-red-600"
            >
              Delete
            </button>
          </div>
        );
      })}
    </div>
  );
}
