from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import httpx  # Use httpx for async HTTP requests
from datetime import datetime
from starlette.staticfiles import StaticFiles

# Load environment variables
load_dotenv()

# Initialize FastAPI and templates
app = FastAPI()

# Mount static files directory
app.mount(
    "/static",
    StaticFiles(directory=os.path.abspath("app/static")),
    name="static",
)

# Initialize templates directory
templates = Jinja2Templates(directory="app/view_templates")

# Environment variables
ADVICE_URL = os.getenv("ADVICE_URL")
NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"  # Build URL correctly

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the index page with server time."""
    server_time = datetime.now().strftime("%H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "server_time": server_time})

@app.get("/advice", response_class=HTMLResponse)
async def get_advice(request: Request):
    """Fetch random advice and render the advice page."""
    async with httpx.AsyncClient() as client:
        response = await client.get(ADVICE_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching advice")
        advice_data = response.json()
        advice = advice_data['slip']['advice']
    return templates.TemplateResponse("advice.html", {"request": request, "advice": advice})

@app.get("/apod", response_class=HTMLResponse)
async def get_apod(request: Request):
    """Fetch Astronomy Picture of the Day (APOD) and render the APOD page."""
    async with httpx.AsyncClient() as client:
        response = await client.get(NASA_APOD_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching APOD")
        apod_data = response.json()
    return templates.TemplateResponse("apod.html", {
        "request": request,
        "title": apod_data.get("title"),
        "image_url": apod_data.get("url"),
        "explanation": apod_data.get("explanation")
    })

@app.get("/params", response_class=HTMLResponse)
async def greet_user(request: Request, name: str = "Guest"):
    """Render the greeting page with the user's name."""
    return templates.TemplateResponse("params.html", {"request": request, "name": name})
