# chat_api.py
import sys
import json
from main import chatbot_reply
from semantic_memory import list_memories, delete_memory

user_input = sys.argv[1]
command = sys.argv[2] if len(sys.argv) > 2 else None

if command == "list":
    print(json.dumps({"memories": list_memories()}, ensure_ascii=False))
    sys.stdout.flush()
    exit()

if command == "delete":
    success = delete_memory(user_input)
    print(json.dumps({"deleted": success}, ensure_ascii=False))
    sys.stdout.flush()
    exit()

reply = chatbot_reply(user_input)
print(json.dumps({"reply": reply}, ensure_ascii=False))
sys.stdout.flush()
