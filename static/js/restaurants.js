// /static/js/restaurants.js
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

function createRestaurantCard(restaurant) {
  const card = document.createElement("div");
  card.className =
    "restaurant-card bg-white p-6 rounded-xl shadow-lg flex flex-col transition-transform duration-300 hover:-translate-y-2 md:w-full";

  const userCount = restaurant.user_count || 0;
  const indicatorColor = userCount > 0 ? "green" : "red";

  // Card Header
  const header = `
    <div class="card-header flex items-center gap-3 mb-4">
      <div class="user-indicator flex items-center justify-center w-7 h-7 text-sm font-bold text-white rounded-full ${indicatorColor}">${userCount}</div>
      <h3 class="text-2xl font-semibold text-slate-700">${restaurant.name}</h3>
    </div>`;

  // Card Body with Menu Sections
  const cardBody = document.createElement("div");
  cardBody.className = "card-body flex-grow space-y-4";

  const createSection = (title, items) => {
    if (!items || items.length === 0) return "";
    return `
      <div class="menu-section mt-6">
        <h4 class="text-lg font-semibold text-slate-600 border-slate-200 pb-1 mb-2">${title}</h4>
        <ul class="list-none p-0 space-y-1">${items
          .map(
            (item) => `
              <li class="w-full text-sm text-slate-500">
                <span class="w-${!item.allergens.length ? 5 : 4}/6">${item.name}</span>
                <span class="w-1/6 ${!item.allergens.length ? "hidden" : ""} text-center">${item.allergens.join(" , ")}</span>
                <span class="w-1/6 text-right">${item.price} CZK</span>
              </li>`,
          )
          .join("")}
        </ul>
      </div>`;
  };

  cardBody.innerHTML += createSection("Soups", restaurant.menu.soups);
  cardBody.innerHTML += createSection("Main Meals", restaurant.menu.main_meals);
  cardBody.innerHTML += createSection("Drinks", restaurant.menu.drinks);

  // Card Footer with Button
  const footer = `
    <div class="card-footer mt-6">
      <button class="join-button w-full bg-green-500 text-white font-bold py-3 px-5 rounded-lg transition-all duration-300 hover:bg-green-600 hover:shadow-md text-lg">Join to ${restaurant.name}</button>
    </div>`;

  card.innerHTML = header;
  card.appendChild(cardBody);
  card.innerHTML += footer;

  card
    .querySelector(".join-button")
    .addEventListener("click", () => joinLunchGroup(restaurant));
  return card;
}

function displayDetailedMenu(menu) {
  const container = document.getElementById("detailed-menu-content");
  container.innerHTML = "";

  const createDetailedItems = (items) => {
    if (!items || items.length === 0) return "";
    return items
      .map(
        (item) => `
          <div class="detailed-menu-item border p-3 rounded-md">
            <div class="detailed-menu-item-header flex justify-between font-semibold">
              <span>${item.name}</span>
              <span>${item.price} CZK</span>
            </div>
            <p class="detailed-menu-item-description text-sm text-slate-500 mt-1">
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
