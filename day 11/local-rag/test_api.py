from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="qwen3.5:2b-q4_K_M",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in one sentence."
        }
    ],
    temperature=0.3,
    reasoning_effort="none",
    max_tokens=100
)

print("Answer:", response.choices[0].message.content)
print("Finish reason:", response.choices[0].finish_reason)
print("Tokens:", response.usage.completion_tokens)