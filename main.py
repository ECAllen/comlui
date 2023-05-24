from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated

import toml
import pandas as pd


app = FastAPI()

app.mount("/static", StaticFiles(directory="static/dist"), name="static")

templates = Jinja2Templates(directory="templates")

# Read in the config file
config = toml.load("config.toml")

# Set the app title from the config file
app_name = config["app"]["name"]

#  Set the app version from the config file
app_version = config["app"]["version"]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# create a post method for the form from index.html
# https://fastapi.tiangolo.com/tutorial/request-forms/
@app.post("/trainer")
async def index(
    data: Annotated[str, Form()],
    features: Annotated[str, Form()],
    target: Annotated[str, Form()],
):
    # features = ["Sex", "Age"]
    return {"data": data, "features": features, "target": target}

@app.post("trainer/data")
async def index(
    data: Annotated[str, Form()],
):
    try:
        train = pd.read_csv(data)
    except FileNotFoundError:
        return {"error": "File not found"}
    return {"data": data}
