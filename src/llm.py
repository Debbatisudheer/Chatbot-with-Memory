# llm.py ✅ (LLM restricted to max 6 words)
from openai import OpenAI
client = OpenAI()

def generate_reply(user_input):

    prompt = f"""
Respond in **maximum 6 words only.**
User: {user_input}
Answer:
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0.5
    )

    reply = response.choices[0].message["content"].strip()

    # ✅ safety cutoff
    return " ".join(reply.split()[:6])
