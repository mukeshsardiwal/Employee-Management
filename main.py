from sanic import Sanic
from sanic.response import json
from tortoise.contrib.sanic import register_tortoise
from utils.middleware import authentication

from config import TORTOISE_ORM

from routes.employee import employee_bp
from routes.device import device_bp
from routes.admin import admin_bp
from routes.auth import auth_bp

app = Sanic("EDMS")
app.middleware("request")(authentication)

app.blueprint(employee_bp)
app.blueprint(device_bp)
app.blueprint(auth_bp)
app.blueprint(admin_bp)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
)

@app.get("/")
async def home(request):
    return json({"Greet": "Welcome To EDMS"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
