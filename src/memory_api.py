from semantic_memory import list_memories
import json

memories = list_memories()

print(json.dumps(memories))  # ALWAYS JSON output
