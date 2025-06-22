import datetime 
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from .joke_agent import joke_agent

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
    This returns the current time in a city in the format "YYYY-MM-DD HH:MM:SS"

    Args:
        city(str): The city to get the current time for.
        timezone(str): The timezone identifier for the city.
    Returns:
        dict: A dictionary containing status and response or error message
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
    name="weather_agent",
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
    ),
    tools=[get_weather, get_current_time],
    sub_agents=[joke_agent]
)