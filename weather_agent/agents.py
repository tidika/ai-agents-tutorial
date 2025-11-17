import json
from openai import OpenAI
from dotenv import load_dotenv
from tools.weather import get_weather
from tools.specs import weather_tool

load_dotenv() #function to load environment variables from a .env file

client = OpenAI()

def run_agent(user_input: str):
    # Create an agent run with the weather tool enabled
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a weather assistant. "
                    "Whenever the user asks about weather, call the get_weather tool."
                )
            },
            { "role": "user", "content": user_input }
        ],
        tools=[weather_tool]
    )

    message = response.choices[0].message

    # If the agent wants to call a tool, run it
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments) # Parse the tool call arguments
            location = args["location"]

            tool_result = get_weather(location)

            # Send tool results back to the model
            second_response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a weather assistant."
                        )
                    },
                    { "role": "user", "content": user_input },
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_result)
                    }
                ]
            )

            return second_response.choices[0].message.content

    # If no tool was needed  
    return message.content

