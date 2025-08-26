# ws/server.py
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from typing import Set, Dict

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

# WebSocket for lunch group registration and live chat
@app.websocket("/ws/{restaurant_name}/{group_name}")
async def websocket_endpoint(websocket: WebSocket, restaurant_name: str, group_name: str):
    # Connect WebSocket
    await websocket.accept()

    # Create or retrieve group for the lunch event
    if group_name not in lunch_groups:
        lunch_groups[group_name] = {
            "restaurant_name": restaurant_name,
            "members": [],
            "chat": []
        }

    group = lunch_groups[group_name]
    group["members"].append(websocket)
    user_counts[restaurant_name] += 1  # Increment the user count

    # Notify members about new arrival
    for member in group["members"]:
        await member.send_text(f"New member joined: {websocket.client.host}. Total: {user_counts[restaurant_name]} people.")

    try:
        while True:
            # Wait for incoming messages in the chat
            data = await websocket.receive_text()
            # Broadcast chat message to the group
            group["chat"].append(data)
            for member in group["members"]:
                await member.send_text(f"{websocket.client.host}: {data}")
    except WebSocketDisconnect:
        group["members"].remove(websocket)
        user_counts[restaurant_name] -= 1  # Decrement the user count
        group["chat"].append(f"{websocket.client.host} has left the group.")
        # Notify other members
        for member in group["members"]:
            await member.send_text(f"{websocket.client.host} has left the group.")

    # Clean up if group is empty
    if len(group["members"]) == 0:
        del lunch_groups[group_name]

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
