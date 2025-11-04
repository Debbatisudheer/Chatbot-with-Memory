from memory import extract_memory, recall_memory

def chatbot_reply(user_input):
    # 1️⃣ Try to recall memory
    remembered = recall_memory(user_input)
    if remembered:
        return remembered

    # 2️⃣ Try to extract/store memory
    learned = extract_memory(user_input)
    if learned:
        return learned

    # 3️⃣ Otherwise general response
    return "Interesting... tell me more."


# ---------------------------------------------------------
# ✅ CLI MODE (ONLY when running manually)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\nChatbot 🤖: Hello! I remember what you tell me.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot 🤖: Bye!")
            break

        reply = chatbot_reply(user_input)
        print("Chatbot 🤖:", reply)
