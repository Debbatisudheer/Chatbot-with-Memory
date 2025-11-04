# chat_api.py  ✅ FIXED VERSION
import sys
import json
from main import chatbot_reply

try:
    user_input = sys.argv[1]  # Read argument from Node
except:
    user_input = ""

reply = chatbot_reply(user_input)

# ✅ ALWAYS return JSON so Node.js can read it
print(json.dumps({"reply": reply}))
sys.stdout.flush()
