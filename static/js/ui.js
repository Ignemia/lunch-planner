// /static/js/ui.js
function joinLunchGroup(restaurant) {
<<<<<<< HEAD
  let username = localStorage.getItem("username");
  if (username === null || username === "") {
    username = prompt("Please enter your name for the chat:");
    if (!username) return;
    localStorage.setItem("username", username);
  }
  
=======
  const username = prompt("Please enter your name for the chat:");
  if (!username) return;

>>>>>>> 880d2e4 (Default functionality (#2))
  // Switch views
  document.getElementById("restaurants-view").classList.add("hidden");
  document.getElementById("joined-view").classList.remove("hidden");
  document.getElementById("joined-header").textContent =
    `Lunch at ${restaurant.name}`;

  displayDetailedMenu(restaurant.menu);
  initializeChat(restaurant.name, username);
}

function leaveGroup() {
  if (currentSocket) {
    currentSocket.close();
    currentSocket = null;
  }
  currentUsername = null;
  document.getElementById("joined-view").classList.add("hidden");
  document.getElementById("restaurants-view").classList.remove("hidden");
  fetchRestaurants();
}