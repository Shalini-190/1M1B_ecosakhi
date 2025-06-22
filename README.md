# EcoSakhi - Your Renewable Energy Assistant

EcoSakhi is an intelligent, full-stack chatbot designed to be your go-to assistant for all things related to renewable energy and sustainable living. It provides users with instant information, calculates energy consumption, and offers personalized tips to save power.

## ✨ Features

- **Conversational Q&A:** Ask questions about various renewable energy sources (Solar, Wind, Hydro, etc.) and get detailed, easy-to-understand answers.
- **Fuzzy String Matching:** The chatbot is resilient to typos and spelling mistakes, understanding the user's intent even with minor errors.
- **Energy Usage Calculator:** Provides a detailed breakdown of daily and monthly energy consumption based on a user's list of household appliances.
- **Personalized Saving Tips:** Suggests relevant energy-saving tips based on the highest-consuming appliances.
- **Renewable Energy Quiz:** An interactive quiz to test your knowledge about green energy, with instant feedback and explanations.
- **Real-time Data Guidance:** Directs users to official government portals like the National Power Portal (NPP) and State Load Despatch Centres (SLDCs) for reliable, real-time energy generation data.

## 🛠️ Tech Stack

- **Backend:** Python with **Flask**
- **Frontend:** HTML, CSS, and vanilla JavaScript
- **NLP/Fuzzy Matching:** `thefuzz` library

## ⚙️ Setup and Installation

To get EcoSakhi running on your local machine, follow these steps:

1.  **Clone the repository (or download the files).**

2.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask backend server:**
    ```bash
    python eco_sakhi_backend.py
    ```

6.  The application will automatically open in your web browser at `http://127.0.0.1:5000`.

## 📂 File Structure

The project is organized into two main parts: a `frontend` and a `backend`.

```
eco-sakhi/
├── backend/
│   ├── eco_sakhi_backend.py  # Main Flask application logic
│   ├── knowledge_base.json   # All chatbot responses, definitions, and data
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── index.html            # The main HTML file for the chat interface
    └── static/
        └── styles.css        # All CSS styles for the application
```

## 🧠 How It Works

The core of the application is the `eco_sakhi_backend.py` script, which uses Flask to serve the frontend and handle chat requests. When a user sends a message, the `process_message` function analyzes it to determine the user's intent using a series of prioritized checks:

1.  **Real-time Data Queries:** It first looks for keywords related to real-time power generation.
2.  **Energy Calculation:** It then checks for patterns indicating a list of appliances to calculate usage.
3.  **Specific Commands:** It looks for direct commands like "quiz" or "energy saving tip".
4.  **Fuzzy Matching:** Finally, it uses the `thefuzz` library to find the best match for definition or greeting-style questions from the `knowledge_base.json` file.

This intent-based logic ensures that the most specific and urgent requests are handled with the highest priority, providing a more intelligent and intuitive user experience. 