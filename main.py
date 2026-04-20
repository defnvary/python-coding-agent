import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt
from call_function import available_functions, call_function

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

    for _ in range(10):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )

        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        function_responses = []
    
        if response.function_calls is not None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
    
                if (
                    function_call_result.parts is None
                    or function_call_result.parts[0].function_response is None
                    or function_call_result.parts[0].function_response.response is None
                ):
                    raise RuntimeError(f"Error: function response error {function_call.name}")
                
    
                if verbose_flag:
                    print(f"-> Calling function: {function_call.name}({function_call.args})")
                    print(f"-> {function_call_result.parts[0].function_response.response["result"]}")
    
                function_responses.append(function_call_result.parts[0])
        
        messages.append(types.Content(role="user", parts=function_responses))
    
        # print(f"API Key: {api_key}")
        print(response.text)
        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return

        if verbose_flag:
            if messages[-1].parts is not None:
                pass
                #print(f"User prompt: {messages[-1].parts[0].text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


        if response.function_calls is None:
            print("all function exhausted.")
            return

    print("maximum number of loop reached")

main()
