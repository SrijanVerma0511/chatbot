import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

key = os.getenv("OPENAI_API_KEY")
print("Loaded:", bool(key))
print("Prefix:", key[:7] if key else "NONE")

client = OpenAI(api_key=key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say hello"}
        ]
    )

    print("SUCCESS")
    print(response.choices[0].message.content)

except Exception as e:
    print("ERROR:")
    print(e)
