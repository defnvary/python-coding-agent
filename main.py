import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 2:
        print("pass a prompt as argument!")
        sys.exit(2)
    prompt = sys.argv[1]

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    if response.function_calls is not None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    # print(f"API Key: {api_key}")
    print(response.text)
    if response is None or response.usage_metadata is None:
        print("response is malformed")
        return

    if verbose_flag:
        if messages[-1].parts is not None:
            print(f"User prompt: {messages[-1].parts[0].text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
