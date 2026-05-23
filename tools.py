def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny with 25°C."


TOOLS = {
    "get_weather": get_weather
}