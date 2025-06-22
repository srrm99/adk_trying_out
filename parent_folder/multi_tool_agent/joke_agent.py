from google.adk.agents import LlmAgent

# Define a joke tool (just a simple Python function)
def python_joke_tool() -> dict:
    return {
        "status": "success",
        "jokes": [
            "Why do Python programmers wear glasses? Because they can't C.",
            "Why did the Python data scientist get thrown out of the restaurant? He kept trying to order arrays.",
            "I told my Python code a joke. It raised an exception.",
            "Why did the developer go broke? Because he used up all his cache.",
            "What's a Python programmer's favorite hangout place? The tuple bar."
        ]
    }

# Create an LlmAgent that uses the joke tool
joke_agent = LlmAgent(
    name="joke_agent",
    model="gemini-2.0-flash",
    description="Agent that tells Python jokes when asked.",
    instruction="You are a fun agent who shares programming jokes. Use the python_joke_tool when the user asks for a joke.",
    tools=[python_joke_tool]
)