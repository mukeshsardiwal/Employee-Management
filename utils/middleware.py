from sanic import Request, response
from utils.jwt import decode_jwt

async def authentication(request: Request):
    public_paths = [
        "/auth/login",
        "/auth/logout",  
        "/device",
        "/employees",
    ]

    if any(request.path.startswith(path) for path in public_paths):
        return 

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return response.json({"error": "Missing or invalid Authorization header"}, status=401)

    token = auth_header[7:]  

    try:
        payload = decode_jwt(token)
        request.ctx.user = payload  
    except Exception:
        return response.json({"error": "Invalid or expired token"}, status=401)
