import random
from typing import List, Dict, Any
from google.adk.agents import LlmAgent

# Comprehensive joke database organized by categories
JOKE_DATABASE = {
    "programming": [
        "Why do Python programmers wear glasses? Because they can't C.",
        "Why did the Python data scientist get thrown out of the restaurant? He kept trying to order arrays.",
        "I told my Python code a joke. It raised an exception.",
        "Why did the developer go broke? Because he used up all his cache.",
        "What's a Python programmer's favorite hangout place? The tuple bar.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, it's a hardware problem.",
        "Why don't programmers like nature? It has too many bugs.",
        "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'",
        "Why did the programmer quit his job? He didn't get arrays (a raise).",
        "What's the object-oriented way to become wealthy? Inheritance.",
        "Why do Java developers wear glasses? Because they don't see sharp (C#).",
        "How do you comfort a JavaScript bug? You console it.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "What do you call a programmer from Finland? Nerdic."
    ],
    "dad_jokes": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I invented a new word: Plagiarism!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
        "Why did the math book look so sad? Because it had too many problems!",
        "What do you call a sleeping bull? A bulldozer!"
    ],
    "tech": [
        "Why was the computer cold? It left its Windows open!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "What do you call a computer superhero? A screensaver!",
        "Why don't robots ever panic? They have nerves of steel!",
        "What's a computer's favorite beat? An algorithm!",
        "Why did the smartphone need glasses? It lost all its contacts!",
        "How does a computer get drunk? It takes screenshots!",
        "Why was the cell phone wearing glasses? It lost its contacts!",
        "What do you call a computer that sings? A Dell!",
        "Why did the computer keep sneezing? It had a virus!"
    ],
    "random": [
        "Why don't elephants use computers? They're afraid of the mouse!",
        "What do you call a fish wearing a crown? A king fish!",
        "Why don't aliens ever land at airports? Because they're looking for space!",
        "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
        "Why don't pencils and erasers get along? Because one makes mistakes and the other fixes them!",
        "What do you call a cow with no legs? Ground beef!",
        "Why did the banana go to the doctor? It wasn't peeling well!",
        "What do you call a dog magician? A labracadabrador!",
        "Why don't mountains ever get cold? They wear snow caps!",
        "What do you call a cat that works for the Red Cross? A first-aid kit!"
    ]
}

def get_joke_by_category(category: str = "random") -> Dict[str, Any]:
    """
    Get a random joke from a specific category.
    
    Args:
        category (str): The category of joke to fetch. 
                       Options: 'programming', 'dad_jokes', 'tech', 'random', 'all'
    
    Returns:
        dict: A dictionary containing the joke and metadata
    """
    category = category.lower()
    
    if category == "all":
        # Get a random joke from any category
        all_jokes = []
        for cat, jokes in JOKE_DATABASE.items():
            all_jokes.extend([(joke, cat) for joke in jokes])
        joke, source_category = random.choice(all_jokes)
        return {
            "status": "success",
            "joke": joke,
            "category": source_category,
            "total_jokes_in_category": len(JOKE_DATABASE[source_category])
        }
    
    elif category in JOKE_DATABASE:
        joke = random.choice(JOKE_DATABASE[category])
        return {
            "status": "success",
            "joke": joke,
            "category": category,
            "total_jokes_in_category": len(JOKE_DATABASE[category])
        }
    else:
        available_categories = list(JOKE_DATABASE.keys()) + ["all"]
        return {
            "status": "error",
            "error_message": f"Category '{category}' not found. Available categories: {', '.join(available_categories)}"
        }

def get_multiple_jokes(count: int = 3, category: str = "random") -> Dict[str, Any]:
    """
    Get multiple random jokes from a specific category.
    
    Args:
        count (int): Number of jokes to fetch (max 10)
        category (str): The category of jokes to fetch
    
    Returns:
        dict: A dictionary containing multiple jokes
    """
    if count > 10:
        count = 10
    elif count < 1:
        count = 1
    
    category = category.lower()
    jokes = []
    
    if category == "all":
        for _ in range(count):
            result = get_joke_by_category("all")
            if result["status"] == "success":
                jokes.append({
                    "joke": result["joke"],
                    "category": result["category"]
                })
    elif category in JOKE_DATABASE:
        available_jokes = JOKE_DATABASE[category].copy()
        random.shuffle(available_jokes)
        for i in range(min(count, len(available_jokes))):
            jokes.append({
                "joke": available_jokes[i],
                "category": category
            })
    else:
        return get_joke_by_category(category)  # Return error message
    
    return {
        "status": "success",
        "jokes": jokes,
        "count": len(jokes),
        "requested_category": category
    }

def get_joke_categories() -> Dict[str, Any]:
    """
    Get all available joke categories and their counts.
    
    Returns:
        dict: Information about available categories
    """
    categories_info = {}
    total_jokes = 0
    
    for category, jokes in JOKE_DATABASE.items():
        categories_info[category] = len(jokes)
        total_jokes += len(jokes)
    
    return {
        "status": "success",
        "categories": categories_info,
        "total_jokes": total_jokes,
        "available_categories": list(JOKE_DATABASE.keys()) + ["all"]
    }

def search_jokes(keyword: str) -> Dict[str, Any]:
    """
    Search for jokes containing a specific keyword.
    
    Args:
        keyword (str): The keyword to search for in jokes
    
    Returns:
        dict: A dictionary containing matching jokes
    """
    keyword = keyword.lower()
    matching_jokes = []
    
    for category, jokes in JOKE_DATABASE.items():
        for joke in jokes:
            if keyword in joke.lower():
                matching_jokes.append({
                    "joke": joke,
                    "category": category
                })
    
    if matching_jokes:
        return {
            "status": "success",
            "keyword": keyword,
            "matches": matching_jokes,
            "count": len(matching_jokes)
        }
    else:
        return {
            "status": "no_matches",
            "keyword": keyword,
            "message": f"No jokes found containing '{keyword}'. Try searching for terms like 'computer', 'programmer', 'bug', etc."
        }

# Enhanced joke agent with multiple tools
joke_agent = LlmAgent(
    name="joke_agent",
    model="gemini-2.0-flash",
    description="A comprehensive joke agent that can tell jokes from various categories, search jokes, and provide entertainment.",
    instruction="""
    You are a fun and entertaining joke agent! Your mission is to bring laughter and joy to users through various types of jokes. 

    Here's what you can do:
    1. Tell random jokes from different categories (programming, dad_jokes, tech, random)
    2. Tell multiple jokes at once for extra laughs
    3. Search for jokes containing specific keywords
    4. Show available joke categories and statistics
    5. Provide personalized joke recommendations

    **Instructions:**
    - Always be enthusiastic and fun in your responses
    - Use emojis occasionally to make interactions more engaging 😄
    - When someone asks for a joke without specifying a category, use 'random' or 'all'
    - If someone seems interested in a particular topic, suggest related joke categories
    - Feel free to add witty commentary before or after jokes
    - If someone asks for programming jokes, use the 'programming' category
    - If someone asks for dad jokes, use the 'dad_jokes' category
    - If someone asks for tech/technology jokes, use the 'tech' category
    - You can tell multiple jokes if someone seems to enjoy them
    - Always encourage users to ask for more jokes or try different categories

    Make every interaction fun and memorable! 🎭
    """,
    tools=[get_joke_by_category, get_multiple_jokes, get_joke_categories, search_jokes]
)