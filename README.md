<div align="center">

# Lunch Group Planner

**A web application for real-time lunch coordination and menu discovery.**

</div>

<p align="center">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/Ignemia/lunch-planner">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Ignemia/lunch-planner">
</p>

## Overview

The **Lunch Group Planner** is a dynamic web application designed to simplify the process of organizing lunch outings. By aggregating daily menus from local restaurants and integrating a real-time chat feature, this platform offers a centralized space for users to coordinate their lunch plans effectively.

---

## Key Features

- **Live Menu Fetching**: 🍽️ Scrapes the latest daily menus from various local restaurants.
- **Restaurant Listings**: 📃 Provides a list of restaurants with menu previews.
- **User Counts**: 👥 Displays how many users are interested in each restaurant.
- **Real-Time Group Chat**: 💬 Each restaurant features its own WebSocket-powered chat room for instant communication.
- **Dynamic UI**: 🖥️ A responsive user interface built with HTML, Tailwind CSS, and vanilla JavaScript.
- **Extensible Architecture**: 🧩 Built with abstract classes to simplify the addition of new restaurant scrapers.

---

## Technology Stack

- **Backend**: Python, FastAPI, Uvicorn
- **WebSockets**: FastAPI's WebSocket support
- **Web Scraping**: BeautifulSoup, Requests
- **Frontend**: HTML5, Tailwind CSS, JavaScript

---

## Project Structure

```

lunch-planner/
├── abstracts/        # Abstract base classes (ARestaurant, AMenu, AMeal)
├── models/           # Concrete data models for meals (Soup, MainMeal, Drink)
├── restaurants/      # Individual Python scripts for each restaurant scraper
├── ws/               # FastAPI server and WebSocket logic
├── static/           # Frontend assets (HTML, CSS, JavaScript)
├── main.py           # Main application entry point
└── requirements.txt  # Project dependencies

````

---

## Setup and Installation

Follow these steps to run the **Lunch Group Planner** locally:

1. **Clone the Repository:**

    - Using SSH:
      ```bash
      git clone --recursive git@github.com:Ignemia/lunch-planner.git
      ```
    - Using HTTPS:
      ```bash
      git clone --recursive https://github.com/Ignemia/lunch-planner.git
      ```
    - Navigate to the project directory:
      ```bash
      cd lunch-planner
      ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    Copy the example `.env` file to create your own configuration:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file to include your specific settings (e.g., geographical coordinates).

5. **Run the Application:**

    ```bash
    python main.py
    ```
    The application will be accessible at `http://127.0.0.1:8000`.

---

## Restaurant Implementations

This repository includes several custom-built scrapers as a demonstration of the Lunch Group Planner’s architecture. The full set of individual restaurant scrapers will not be publicly maintained. However, the provided examples serve as a solid foundation for developers interested in extending the platform.

---

## Adding a New Restaurant

To integrate a new restaurant into the application, follow these steps:

1. **Create a New Scraper:**
    - Create a new Python file in the `restaurants/` directory.

2. **Implement the Restaurant Class:**
    - Define a class that inherits from the `ARestaurant` abstract class.
    - Implement the `fetch_menu` method to scrape the restaurant's website.
    - Implement the `parse_menu` method to process the scraped HTML and structure the menu.

3. **Integrate the New Restaurant:**
    - Import your new restaurant class and add it to the `initialize_restaurants` function in `main.py`.

---

## Contributing

We welcome contributions to the Lunch Group Planner! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write tests for your changes (if applicable).
4. Ensure all tests pass.
5. Submit a pull request with a clear description of your changes.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.