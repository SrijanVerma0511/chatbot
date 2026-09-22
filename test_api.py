import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

key = os.getenv("GEMINI_API_KEY")
print("Loaded:", bool(key))
print("Prefix:", key[:7] if key else "NONE")

if not key:
    print("ERROR: GEMINI_API_KEY is not set.")
    exit(1)

client = genai.Client(api_key=key)
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

try:
    print(f"Testing Gemini model: {model_name}...")
    response = client.models.generate_content(
        model=model_name,
        contents="Say hello in one short sentence.",
    )

    print("SUCCESS!")
    print("Response:", response.text)

except Exception as e:
    print("ERROR:")
    print(e)
