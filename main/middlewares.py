import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Omitir las rutas innecesarias
        excluded_paths = ["/api/user/login", "/api/user/register"]

        if request.path in excluded_paths:
            return self.get_response(request)

        # Sacar token del encabezado
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({
                "status": "error",
                "message": "Falta el token de autenticacion"
            })

        # token = auth_header
        token = auth_header.removeprefix("Bearer ").strip()

        try:
            # decodificar el token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms = ["HS256"])
            
            # agregar datos del usuario a request
            request.user = payload

        except jwt.ExpiredSignatureError:
            return JsonResponse({
                "status": "error",
                "message": "El token a caducado"
            })
        except jwt.InvalidTokenError:
            return JsonResponse({
                "status": "error",
                "message": "Token invalido"
            })

        # continuar con la solicitud 
        response = self.get_response(request)
        return response

