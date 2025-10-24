# test_ollama_direct.py
import ollama

try:
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": "Привет!"}],
        options={"temperature": 0.7}
    )
    print("✅ Ответ от Ollama:", response['message']['content'])
except Exception as e:
    print("❌ Ошибка:", e)
    import traceback
    traceback.print_exc()