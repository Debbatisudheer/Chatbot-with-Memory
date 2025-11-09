import ChatWindow from "./components/ChatWindow";
import MemoryPanel from "./components/MemoryPanel";

export default function App() {
  return (
    <div className="flex h-screen w-screen">
      <ChatWindow />
      <MemoryPanel /> {/* ✅ Memory panel always visible */}
    </div>
  );
}
