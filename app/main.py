import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load model list from config.json
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    model = config_data["model"]

image_names = []
idx = 0

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/getData")
async def get_data():
    global image_names
    global idx

    if not image_names:
        image_dir = os.path.join("static", "images", model[0])
        if os.path.exists(image_dir):
            image_names = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', 'JPG', 'jpeg', '.png'))]
            image_names = sorted(image_names, key=lambda x: x.lower())

    data = {
        "imageBoxes": [
            {
                "elements": [
                    {"image": f"static/images/{name}/{image_names[idx]}", "title": name} for name in model
                ],
                "title": f"{idx}-{image_names[idx]}",
            },
        ]
    }

    return JSONResponse(content=data)

@app.get("/api/changeIndex")
async def change_index(direction: str):
    global idx

    if direction == "next":
        idx = (idx + 1) % len(image_names)
    elif direction == "prev":
        idx = (idx - 1 + len(image_names)) % len(image_names)

    return JSONResponse(content={"message": "Index updated"})

