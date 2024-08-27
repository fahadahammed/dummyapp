"""DummyApp

Return: Hit Count
"""

import datetime
import os
import time
import random
import socket
import json

from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run


the_hostname = socket.gethostname()
service_name = os.getenv("SERVICE_NAME", "DummyApp")
STARTUP_DELAY = int(os.getenv("STARTUP_DELAY", f"{random.randint(20, 30)}"))
LIVENESS_DELAY_COUNTER = int(os.getenv("LIVENESS_DELAY_COUNTER", "2"))
READINESS_DELAY_COUNTER = int(os.getenv("LIVENESS_DELAY_COUNTER", "2"))
HIT_COUNT = int(os.getenv("HIT_COUNT", "0"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
TIMEOUT_VALUE = int(os.getenv("TIMEOUT_VALUE", "0"))

app = FastAPI()


def check_odd_or_even(number):
    if number % 2 == 0:
        return "EVEN"
    return "ODD"


def hit_count():
    global HIT_COUNT
    HIT_COUNT = HIT_COUNT + 1
    return HIT_COUNT


# Static and Template
def prepare_static_template():
    if not os.path.exists("static"):
        os.makedirs("static")
    if not os.path.exists("templates"):
        os.makedirs("templates")
    with open("templates/index.html", "w+", encoding="utf-8") as itemplate:
        itemplate.write('''
        <html>
<head>
    <title>{{data['service']}}</title>
</head>
<body>
    <h1>{{message}}</h1>
    <p align='center'>
    <h3>{{data['service']}}</h3>
    <h3>{{data['time']}}</h3>
    <h3>{{data['version']}}</h3>
    <h3>{{data['service']}}</h3>
    <h2>{{data['hit_count']}}</h2>
    </p>
</body>
</html>
        ''')


prepare_static_template()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request, html: bool = False):
    result = hit_count()
    to_return = {
        "message": f"Hello World from {service_name}:{the_hostname}!",
        "data": {
            "service": f"{service_name}",
            "time": datetime.datetime.utcnow(),
            "version": os.getenv("VERSION", "v1"),
            "environment": ENVIRONMENT,
            "hit_count": result
        }
    }
    if html:
        return templates.TemplateResponse(
            request=request, name="index.html", context=to_return
        )
    return to_return


@app.get("/probe/liveness")
def probe_liveness():
    if check_odd_or_even(random.choice(list(range(LIVENESS_DELAY_COUNTER)))) == "ODD":
        return False
    return Response(json.dumps({"message": "I am alive!"}), status_code=200)


@app.get("/probe/readiness")
def probe_readiness():
    if check_odd_or_even(random.choice(list(range(READINESS_DELAY_COUNTER)))) == "ODD":
        return False
    return Response(json.dumps({"message": "I am ready!"}), status_code=200)


@app.get("/probe/startup")
def probe_startup():
    """Startup Probe
    Return: It will just return after waiting some time depending on STARTUP_DELAY
    that it has started.
    """
    
    time.sleep(int(STARTUP_DELAY))
    return Response(json.dumps({"message": "I have started!"}), status_code=200)


@app.get("/timeout_check")
def timeout_check(request: Request, html: bool = False):
    timeout_value = TIMEOUT_VALUE
    to_return = {
        "message": f"Hello World from {service_name}:{the_hostname}!",
        "data": {
            "service": f"{service_name}",
            "time": datetime.datetime.utcnow(),
            "version": os.getenv("VERSION", "v1"),
            "environment": ENVIRONMENT,
            "timeout": f"It took {timeout_value} seconds to load."
        }
    }
    if html:
        return templates.TemplateResponse(
            request=request, name="index.html", context=to_return
        )
    return to_return


if __name__ == "__main__":
    run(
        app="__main__:app",
        reload=True, port=int(os.getenv("UVICORN_PORT", "7551")),
        host=os.getenv("UVICORN_HOST", "0.0.0.0")
    )
