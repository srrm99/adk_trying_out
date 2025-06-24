import datetime 
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .joke_agent import joke_agent
from .search_agent import search_agent
from google.genai import types
from google.adk.tools import agent_tool

def get_weather(city: str) -> dict:
    """
    This returns the weather in a city.
    Args:
        city(str): The city to get the weather for.
    Returns: 
        dict: A dictionary containing status or result or error message
    """

    if city.lower() == "mumbai":
        return {
            "status": "success",
            "result": {
                "temperature": 25,
                "humidity": 50,
                "wind_speed": 10,
                "description": "sunny",
            },
        }
    else:
        return {
            "status":"error",
            "error_message": f"weather for city {city} not found"}

def get_current_time(city: str, timezone: str) -> dict:
    """
    Get the current time for a specified city using its timezone.

    Returns the current time in the format "YYYY-MM-DD HH:MM:SS TZ±HHMM" 
    (e.g. "2024-02-14 13:45:30 IST+0530"). Currently only supports Mumbai and Delhi.

    Args:
        city (str): The city to get the current time for. Must be either "Mumbai" or "Delhi" (case-insensitive).
        timezone (str): The timezone identifier for the city (e.g. "Asia/Kolkata"). Must be a valid IANA timezone name.

    Returns:
        dict: A dictionary containing:
            - On success: {"status": "success", "result": {"time": "<formatted time string>"}}
            - On error: {"status": "error", "error_message": "<error details>"}

    Example:
        >>> get_current_time("Mumbai", "Asia/Kolkata")
        {
            "status": "success", 
            "result": {
                "time": "The current time in Mumbai is 2024-02-14 13:45:30 IST+0530"
            }
        }
    """

    if city.lower() == "mumbai" or city.lower() == "delhi":
        now = datetime.datetime.now(ZoneInfo(timezone))
        return {
            "status": "success",
            "result": {
                "time": f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
            }
        }
    else:
        return {
            "status": "error",
            "error_message": f"Time for city {city} not found"
        }

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the weather and timein a city."
    ),
    instruction=(
        "You are a helpful assistant that provides accurate weather and time information for Indian cities. "
        "When calling the `get_current_time` tool, ensure you pass both `city` and a valid timezone identifier (e.g., 'Asia/Kolkata' for IST). "
        "When calling the `get_weather` tool, only the `city` argument is required. "
        "If the city is not supported, return a helpful error message indicating that data is unavailable."
        "If the user asks for jokes, delegate the query to the `joke_agent` using transfer_to_agent."
        "You have also have access to google search tool. You can use it to search the internet for information."
    ),
    tools=[agent_tool.AgentTool(agent=search_agent),get_weather, get_current_time],
    sub_agents=[joke_agent]
)
