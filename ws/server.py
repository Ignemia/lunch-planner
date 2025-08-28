# ws/server.py
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from typing import Set, Dict
from collections import defaultdict

# Import ARestaurant abstract class
from abstracts.ARestaurant import ARestaurant
from abstracts.AMenu import AMenu
from abstracts.AMeal import AMeal
app = FastAPI()

# Serve static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dynamic management of restaurants and user groups
REGISTERED_RESTAURANTS: Set[ARestaurant] = set()
lunch_groups: Dict[str, Dict] = {}
user_counts: Dict[str, int] = {}

def initialize_restaurants(initialize_fn):
    global REGISTERED_RESTAURANTS, user_counts
    # Dynamically initialize all restaurants
    REGISTERED_RESTAURANTS = initialize_fn()

    # Initialize user counts for each restaurant
    for restaurant in REGISTERED_RESTAURANTS:
        user_counts[restaurant.get_name()] = 0  # Set the initial user count to 0
        restaurant.fetch_menu()

# FastAPI routes and endpoints
@app.get("/available-restaurants")
async def get_available_restaurants():
    restaurants_data = []
    for restaurant in REGISTERED_RESTAURANTS:
        menu = restaurant.get_menu()

        if menu is None:
            menu_data = {"drinks": [], "soups": [], "main_meals": []}
        else:
            # Generate the menu data dynamically
            menu_data = generate_menu(menu)

        restaurants_data.append({
            "name": restaurant.get_name(),
            "user_count": user_counts[restaurant.get_name()],
            "menu": menu_data  # This will be used to display menu data
        })

    return restaurants_data

def generate_menu(menu: AMenu):
    menu_data = {
        "drinks": [],
        "soups": [],
        "main_meals": []
    }

    # Add drinks from the menu
    for drink in menu.drinks:
        menu_data["drinks"].append({
            "name": drink.name,
            "price": drink.price,
            "allergens": [a+1 for a in range(14) if drink.allergens[a]],
            "description": drink.detailed_description
        })

    # Add soups from the menu
    for soup in menu.meals["soups"]:
        menu_data["soups"].append({
            "name": soup.name,
            "price": soup.price,
            "allergens": [a+1 for a in range(14) if soup.allergens[a]],
            "description": soup.detailed_description
        })

    # Add main meals from the menu
    for meal in menu.meals["main_meals"]:
        menu_data["main_meals"].append({
            "name": meal.name,
            "price": meal.price,
            "allergens": [a+1 for a in range(14) if meal.allergens[a]],
            "description": meal.detailed_description
        })

    return menu_data

@app.get("/{restaurant_name}/menu")
async def get_menu(restaurant_name: str):
    restaurant = next((r for r in REGISTERED_RESTAURANTS if r.get_name() == restaurant_name), None)
    if restaurant:
        menu = restaurant.get_menu()
        if menu is None:
            menu_data = {"drinks": [], "soups": [], "main_meals": []}  # Default empty menu
        else:
            menu_data = generate_menu(menu)
        return {"menu": menu_data}
    else:
        return {"error": "Restaurant not found"}

@app.get("/{restaurant_name}/{menu_item_id}/description")
async def get_menu_item_description(restaurant_name: str, menu_item_id: int):
    restaurant = next((r for r in REGISTERED_RESTAURANTS if r.get_name() == restaurant_name), None)
    if restaurant:
        menu_item = list(restaurant.get_menu().meals["soups"] | restaurant.get_menu().meals["main_meals"] | restaurant.get_menu().drinks)[menu_item_id - 1]
        return {"description": menu_item.detailed_description}
    else:
        return {"error": "Restaurant or menu item not found"}

@app.get("/{restaurant_name}/{menu_item_id}/allergens")
async def get_menu_item_allergens(restaurant_name: str, menu_item_id: int):
    restaurant = next((r for r in REGISTERED_RESTAURANTS if r.get_name() == restaurant_name), None)
    if restaurant:
        menu_item = list(restaurant.get_menu().meals["soups"] | restaurant.get_menu().meals["main_meals"] | restaurant.get_menu().drinks)[menu_item_id - 1]
        return {"allergens": [a+1 for a in range(14) if menu_item.allergens[a]]}
    else:
        return {"error": "Restaurant or menu item not found"}


# Store lunch groups and user counts
lunch_groups = defaultdict(lambda: {"members": [], "chat": []})
user_counts = {}

@app.websocket("/ws/{restaurant_name}")
async def websocket_endpoint(websocket: WebSocket, restaurant_name: str, user_name: str = Query(...)):
    # Accept WebSocket connection
    await websocket.accept()

    # Check if the user already exists in the group
    group = lunch_groups.setdefault(restaurant_name, {"members": [], "chat": []})
    if user_name not in [member["name"] for member in group["members"]]:
        group["members"].append({"name": user_name, "websocket": websocket})
        user_counts[restaurant_name] = len(group["members"])

    for member in group["members"]:
            if member["name"] == user_name:
                for chat_message in group["chat"]:
                    await member["websocket"].send_json(chat_message)

    # Notify all members about the new arrival
    for member in group["members"]:
        await member["websocket"].send_json({
            "sender": "system",
            "message": f"{user_name} has joined the group! Total: {user_counts[restaurant_name]} people."
        })

    try:
        while True:
            # Wait for incoming messages
            data = await websocket.receive_text()

            # Check if it's a command
            if data.startswith("/"):
                command = data[1:].strip()  # Remove '/' to get the command
                await handle_command(command, restaurant_name, user_name)
            else:
                # Regular chat message
                chat_message = {"sender": user_name, "message": data}
                group["chat"].append(chat_message)
                # Broadcast the chat message to all members
                for member in group["members"]:
                    if member["name"] == user_name:
                        continue
                    await member["websocket"].send_json(chat_message)

    except WebSocketDisconnect:
        # Handle user disconnection
        group["members"] = [member for member in group["members"] if member["name"] != user_name]
        user_counts[restaurant_name] = len(group['members'])
        for member in group["members"]:
            await member["websocket"].send_json({
                "sender": "system",
                "message": f"{user_name} has left the group."
            })

        # Cleanup if no members are left in the group
        if len(group["members"]) == 0:
            del lunch_groups[restaurant_name]


# Command handler example (e.g., for '/kick')
async def handle_command(command: str, restaurant_name: str, user_name: str):
    group = lunch_groups[restaurant_name]

    if command.startswith("kick"):
        _, target_user = command.split(" ", 1)
        target_user = target_user.strip()

        # Find the target user and remove them
        target_member = next((member for member in group["members"] if member["name"] == target_user), None)
        if target_member:
            group["members"].remove(target_member)
            user_counts[restaurant_name] -= 1
            await target_member["websocket"].send_text(f"You have been kicked out by {user_name}.")
            # Notify others
            for member in group["members"]:
                await member["websocket"].send_text(f"{user_name} kicked {target_user} out of the group.")
        else:
            # If the user is not found
            await group["members"][0]["websocket"].send_text(f"User {target_user} not found in the group.")


# Serve the main HTML page
@app.get("/")
async def serve_frontend():
    with open("static/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# Function to start the server
def start(initialize_fn):
    # Directly call initialize_fn to load the restaurants
    initialize_restaurants(initialize_fn)
    uvicorn.run(app, host="0.0.0.0", port=8000)
