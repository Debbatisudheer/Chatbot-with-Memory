import sys
from semantic_memory import delete_memory

memory_id = sys.argv[1]
delete_memory(memory_id)
print("OK")
