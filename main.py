from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated

import toml
import os
from pathlib import Path

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

def data_file_checks(fname):
    if fname.endswith(".csv") and os.path.isfile(fname):
        return True
    else: 
        return False

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)



# create a post method for the form from index.html
# https://fastapi.tiangolo.com/tutorial/request-forms/
@app.post("/trainer")
async def index(
    train_file: Annotated[str, Form()],
    test_file: Annotated[str, Form()],
    features: Annotated[str, Form()], 
):
    features = features.split() 

    if data_file_checks(train_file):
        train = pd.read_csv(train_file)
    else:
        raise HTTPException(status_code=400, detail=f"{train_file} File not found")

    if data_file_checks(test_file):
        test = pd.read_csv(test_file)
    else:
        raise HTTPException(status_code=400, detail=f"{test_file} File not found")

    X = pd.get_dummies(train[features])
    X_test = pd.get_dummies(test[features])
    y = train["Survived"]

    age_mean = int(X.Age.mean())
    X.Age = X.Age.fillna(age_mean)

    age_mean = int(X_test.Age.mean())
    X_test.Age = X_test.Age.fillna(age_mean)

    forest = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)

    return {"train data": train_file, "features": features}


@app.post("/trainer/data/train")
async def index( 
    request: Request,
    train_file: Annotated[str, Form()],
):
    # TODO add train specifc tests
    context = {"request": request, "train_file": train_file}
    if data_file_checks(train_file): 
        return templates.TemplateResponse("partials/train_data_form.html", context)
    else:
        return templates.TemplateResponse("partials/error_train_data_form.html", context)


@app.post("/trainer/data/test")
async def index( 
    request: Request,
    test_file: Annotated[str, Form()],
):
    # TODO add test specifc tests
    context = {"request": request, "test_file": test_file}
    if data_file_checks(test_file): 
        return templates.TemplateResponse("partials/test_data_form.html", context)
    else:
        return templates.TemplateResponse("partials/error_test_data_form.html", context)

