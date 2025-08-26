// static/main.js
let currentSocket = null;
let currentUsername = null;

document.addEventListener("DOMContentLoaded", function () {
  fetchRestaurants();
  document.getElementById("leave-button").addEventListener("click", leaveGroup);
});

// Fetch and display all qualifying restaurants
async function fetchRestaurants() {
  try {
    const response = await fetch("/available-restaurants");
    const restaurants = await response.json();
    const container = document.getElementById("restaurants-list");
    container.innerHTML = "";

    restaurants.forEach((restaurant) => {
      // Only process restaurants that actually have menu items
      const hasMenu =
        restaurant.menu &&
        (restaurant.menu.soups?.length ||
          restaurant.menu.main_meals?.length ||
          restaurant.menu.drinks?.length);

      if (hasMenu) {
        container.appendChild(createRestaurantCard(restaurant));
      }
    });
  } catch (error) {
    console.error("Failed to fetch restaurant data:", error);
  }
}

// Create the "island" card for a single restaurant
function createRestaurantCard(restaurant) {
  const card = document.createElement("div");
  card.className = "restaurant-card";

  const userCount = restaurant.user_count || 0;
  const indicatorColor = userCount > 0 ? "green" : "red";

  // Card Header
  const header = `
        <div class="card-header">
            <div class="user-indicator ${indicatorColor}">${userCount}</div>
            <h3>${restaurant.name}</h3>
        </div>`;

  // Card Body with Menu Sections
  const cardBody = document.createElement("div");
  cardBody.className = "card-body";

  const createSection = (title, items) => {
    if (!items || items.length === 0) return "";
    return `
            <div class="menu-section">
                <h4>${title}</h4>
                <ul>${items.map((item) => `<li><span>${item.name}</span><span>${item.price} CZK</span></li>`).join("")}</ul>
            </div>`;
  };

  cardBody.innerHTML += createSection("Soups", restaurant.menu.soups);
  cardBody.innerHTML += createSection("Main Meals", restaurant.menu.main_meals);
  cardBody.innerHTML += createSection("Drinks", restaurant.menu.drinks);

  // Card Footer with Button
  const footer = `
        <div class="card-footer">
            <button class="join-button">Join to ${restaurant.name}</button>
        </div>`;

  card.innerHTML = header;
  card.appendChild(cardBody);
  card.innerHTML += footer;

  card
    .querySelector(".join-button")
    .addEventListener("click", () => joinLunchGroup(restaurant));
  return card;
}

// Handle the transition to the "joined" view
function joinLunchGroup(restaurant) {
  const username = prompt("Please enter your name for the chat:");
  if (!username) return;
  currentUsername = username;

  // Switch views
  document.getElementById("restaurants-view").classList.add("hidden");
  document.getElementById("joined-view").classList.remove("hidden");
  document.getElementById("joined-header").textContent =
    `Lunch at ${restaurant.name}`;

  displayDetailedMenu(restaurant.menu);
  initializeChat(restaurant.name, username);
}

// Handle leaving a group and returning to the main view
function leaveGroup() {
  if (currentSocket) {
    currentSocket.close();
    currentSocket = null;
  }
  currentUsername = null;
  document.getElementById("joined-view").classList.add("hidden");
  document.getElementById("restaurants-view").classList.remove("hidden");
  // We fetch again to get updated user counts
  fetchRestaurants();
}

// Populate the detailed menu in the "joined" view
function displayDetailedMenu(menu) {
  const container = document.getElementById("detailed-menu-content");
  container.innerHTML = "";

  const createDetailedItems = (items) => {
    if (!items || items.length === 0) return "";
    return items
      .map(
        (item) => `
            <div class="detailed-menu-item">
                <div class="detailed-menu-item-header">
                    <span>${item.name}</span>
                    <span>${item.price} CZK</span>
                </div>
                <p class="detailed-menu-item-description">
                    ${item.description || "No description available."}
                    ${item.allergens?.length ? `<strong>Allergens: ${item.allergens.join(", ")}</strong>` : ""}
                </p>
            </div>
        `,
      )
      .join("");
  };

  container.innerHTML += createDetailedItems(menu.soups);
  container.innerHTML += createDetailedItems(menu.main_meals);
  container.innerHTML += createDetailedItems(menu.drinks);
}

// Set up the chat functionality and WebSocket connection
function initializeChat(restaurantName, username) {
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  chatMessages.innerHTML = ""; // Clear old messages

  const socket = new WebSocket(
    `ws://localhost:8000/ws/${restaurantName}/${username}`,
  );
  currentSocket = socket;

  socket.onopen = () => {
    console.log(`Connected to chat for ${restaurantName}`);
    addChatMessage(
      { sender: "System", message: "You have joined the chat." },
      "other",
    );
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const type = data.sender === currentUsername ? "self" : "other";
    addChatMessage(data, type);
  };

  socket.onclose = () => {
    console.log("Connection closed");
    addChatMessage(
      { sender: "System", message: "You have been disconnected." },
      "other",
    );
  };

  chatForm.onsubmit = (event) => {
    event.preventDefault();
    const message = chatInput.value;
    if (message.trim()) {
      socket.send(message);
      addChatMessage({ sender: currentUsername, message }, "self");
      chatInput.value = "";
    }
  };
}

// Helper to add a message to the chat UI
function addChatMessage(data, type) {
  const chatMessages = document.getElementById("chat-messages");
  const messageElement = document.createElement("div");
  messageElement.className = `chat-message ${type}`;
  const sender = type === "self" ? "You" : data.sender;
  messageElement.innerHTML = `<strong>${sender}:</strong><p>${data.message}</p>`;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
}
