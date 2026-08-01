import os
from dotenv import load_dotenv
from groq import Groq

def test_connection():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your-groq-api-key-here":
        print("ERROR: Invalid or missing API key in .env")
        return

    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say 'LLM connection is successful!' if you receive this message. Reply with only that sentence.",
                }
            ],
            model="llama-3.1-8b-instant",
        )
        print("Success! Response from Groq:")
        print(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"ERROR connecting to Groq: {e}")

if __name__ == "__main__":
    test_connection()
