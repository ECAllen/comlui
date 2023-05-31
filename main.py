from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated

import toml
import os

from sklearn.ensemble import RandomForestClassifier
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
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


# create a post method for the form from index.html
# https://fastapi.tiangolo.com/tutorial/request-forms/
@app.post("/trainer")
async def index(
    data: Annotated[str, Form()],
    features: Annotated[str, Form()], 
    target: Annotated[str, Form()],
):
    features = features.split() 

    if data.endswith(".csv") and os.path.isfile(data):
        train = pd.read_csv(data)

    if data.endswith(".csv") and os.path.isfile(data):
        test = pd.read_csv("./test.csv")

    X = pd.get_dummies(train[features])
    X_test = pd.get_dummies(test[features])
    y = train["Survived"]

    age_mean = int(X.Age.mean())
    X.Age = X.Age.fillna(age_mean)

    age_mean = int(X_test.Age.mean())
    X_test.Age = X_test.Age.fillna(age_mean)

    forest = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)

    return {"data": data, "features": features, "target": target}


@app.post("/trainer/data/{data_split}")
async def index( 
    request: Request,
    data_file: Annotated[str, Form()],
):
    context = {"request": request, "data_file": data_file}
    if data_file.endswith(".csv") and os.path.isfile(data):
        return templates.TemplateResponse(f"partials/{data_split}_data_form.html", context)
    else:
        return templates.TemplateResponse(f"partials/error_{data_split}_data_form.html", context)


