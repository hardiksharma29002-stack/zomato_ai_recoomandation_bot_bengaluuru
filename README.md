# Zomato AI Restaurant Recommendation System
🚀 **Live Demo:** [https://zomato-ai-recoomandation-bot-bengaluuru.onrender.com/](https://zomato-ai-recoomandation-bot-bengaluuru.onrender.com/)

An AI-powered restaurant recommendation system that helps you find your next favorite dining spot. By combining real restaurant data from Zomato with the intelligence of modern Large Language Models (LLMs), this bot analyzes your location, budget, and cuisine preferences to provide highly personalized, human-like restaurant recommendations with detailed explanations of *why* you will love them!

Built with React (Vite) on the frontend and FastAPI on the backend.

## 📊 Dataset Information
The application utilizes a sampled subset (5,000 restaurants) of the comprehensive **Bengaluru Zomato Restaurant Data**. 
- **Source Data:** Contains crucial features like restaurant names, locations, cuisines, approximate cost for two, and user ratings.
- **How it works:** The data is cleaned and processed using Pandas. When a user submits their preferences (e.g., location and budget), the system first filters the dataset using Pandas to find realistic matches. The resulting candidate restaurants are then passed into the LLM context window to generate the final personalized recommendations.
- **Optimization:** To allow for fast, free cloud hosting with limited memory, the data is served via a pre-processed, lightweight CSV subset that loads instantly into memory.

## Quickstart

### Prerequisites
- Python 3.10+
- Node.js (v16+)
- Virtual environment tool (e.g., `venv`)

### Running Locally (Windows / macOS / Linux)
The easiest way to start the application locally is using the provided `start.py` script. This will automatically build the React frontend and serve it via the FastAPI backend, and then open your browser.

1. **Clone the repository and navigate to it.**
2. **Setup your environment variables:**
   Ensure you have a `.env` file in the root directory with your API keys. You can copy the example:
   ```bash
   copy .env.example .env
   ```
3. **Run the script:**
   From your terminal, run:
   ```bash
   python start.py
   ```
4. **View the app:**
   Your browser will automatically open to [http://127.0.0.1:8000](http://127.0.0.1:8000). Keep the terminal open while using the app!

### Manual Installation & Running

**1. Backend Setup:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

**2. Frontend Setup (Development Mode):**
```bash
cd frontend
npm install
npm run dev
```

**3. Run Backend API:**
```bash
python -m src.main --server
```

## Troubleshooting Empty Dropdowns (City/Cuisines)
If your City and Cuisine dropdowns are empty, it means the React frontend cannot communicate with the backend API to fetch the metadata. Ensure that you are running the backend server on port 8000 (`python -m src.main --server`) alongside the frontend. The `run_local.bat` script handles this automatically for you.

## Project Structure
- `src/data/`: Data ingestion, loading, and preprocessing (Hugging Face Datasets).
- `src/models/`: Pydantic models for preferences and recommendations.
- `src/api/`: FastAPI routes and server configuration.
- `src/services/`: Core logic including filtering, prompting, and LLM calls.
- `frontend/`: React + Vite application for the user interface.
