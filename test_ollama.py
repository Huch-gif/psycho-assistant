import ollama

response = ollama.chat(
    model="llama3:latest",
    messages=[{"role": "user", "content": "Привет! Как дела?"}]
)
print(response['message']['content'])