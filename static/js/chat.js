// /static/js/chat.js
let currentSocket = null;
let currentUsername = null;

function initializeChat(restaurantName, username) {
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  chatMessages.innerHTML = ""; // Clear old messages

  const socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/${restaurantName}/${username}`,
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

function addChatMessage(data, type) {
  const chatMessages = document.getElementById("chat-messages");
  const messageElement = document.createElement("div");
  messageElement.className = `p-3 rounded-lg max-w-xs chat-message ${type == "self" ? "self bg-green-100 text-green-900 self-end" : "other bg-slate-200 text-slate-900 self-start"}`;
  const sender = type === "self" ? "You" : data.sender;
  messageElement.innerHTML = `<strong>${sender}:</strong><p>${data.message}</p>`;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
}

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
