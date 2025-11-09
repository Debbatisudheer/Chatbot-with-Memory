from memory import extract_memory, recall_memory
from semantic_memory import add_semantic_memory, search_semantic_memory

def chatbot_reply(user_input):

    text = user_input.lower()

    # ✅ First check structured memory
    structured = recall_memory(text)
    if structured:
        return structured

    # ✅ If user is giving memory → store it
    learned = extract_memory(text)
    if learned:
        add_semantic_memory(text)  # Store also in vector DB
        return learned

    # ✅ Then semantic memory
    semantic = search_semantic_memory(text)
    if semantic:
        return semantic

    # ✅ Default
    add_semantic_memory(text)
    return "interesting... tell me more."
