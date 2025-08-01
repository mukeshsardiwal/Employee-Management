from sanic import response, Blueprint, Request
from utils.auth import verify_password
from utils.jwt import generate_jwt, decode_jwt
from models.admin import Admin

auth_bp = Blueprint("auth", url_prefix="/auth")

# Admin Login Only
@auth_bp.route("/login", methods=["POST"])
async def login(request: Request):
    data = request.json
    username = data.get("username")  
    password = data.get("password")

    if not username or not password:
        return response.json({"error": "Username and password required"}, status=400)

    admin = await Admin.get_or_none(username=username)
    
    if not admin or not verify_password(password, admin.password):
        return response.json({"error": "Invalid credentials"}, status=401)

    token = generate_jwt()  
    return response.json({"token": token})

# Logout
@auth_bp.post("/logout")
async def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return response.json(
            {"error": "Missing or invalid Authorization header"}, status=401
        )

    token = auth_header[7:] 

    try:
        payload = decode_jwt(token)
        return response.json({"message": "Logged out successfully"})
    except Exception:
        return response.json({"error": "Invalid or expired token"}, status=401)
