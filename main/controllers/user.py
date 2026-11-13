from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from main.models import User
from main.validator import UserValidatorForm
from main.serializers import UserSerializer
from main.helpers import Helpers
import json

@csrf_exempt
def save(request):
    if request.method == "POST":

        # Sacar el password del usuario y cifrarlo
        # password = request.POST.get("password", "")
        data = json.loads(request.body)
        password = data.get("password", "")
        passwordEncoded = make_password(password)        

        # Validar los datos del usuario
        form = UserValidatorForm(data)


        if form.is_valid():

            # Crear objeto con los datos 
            user = User(
                name = data.get("name", ""),
                surname = data.get("surname", ""),
                nick = data.get("nick", "").lower(),
                email = data.get("email", "").lower(),
                bio = data.get("bio", ""),
                password = passwordEncoded
            )

        else: 
            dataResponse = {
                "status": "error",
                "message": "Error de validacion"
            }

        
        # Comprobar si no existe el usuario en la bd
        try:
            usersFinds = User.objects.filter(Q(email = user.email.lower()) | Q(nick = user.nick.lower()) )
        except:
            dataResponse = {
                "status": "error",
                "message": "Error al comprobar usuario"
            }

        # Si existe da error
        if len(usersFinds) > 0:
            dataResponse = {
                "status": "error",
                "message": "El usuario ya existe en la bd"
            }
        else:
            # Si NO existe se crea con estos datos
            user.save()
            userSz = UserSerializer(user, many=False)
            dataResponse = {
                "status": "success",
                "message": "Validacion completada",
                "user": userSz.data
            }

        # Devolver respuesta
        return JsonResponse(dataResponse)
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })
    

      

@csrf_exempt
def login(request):
    if request.method == "POST":

        data = json.loads(request.body)

        # Verificar si me llegan los datos para el login
        if data.get("email", "") and data.get("password", ""): 

            # Sacar valores del email y el password
            email = data.get("email", "")
            password = data.get("password", "")

            # Buscar usuario con el correo recibido
            userLogin = User.objects.filter(email = email)[0]

            # Sacar password cifrado
            passwordEncoded = userLogin.password

            # Verificar el password para ver si coincide
            if check_password(password, passwordEncoded):

                # Serializar usuario para decolver el json 
                userLoginS = UserSerializer(userLogin, many=False)

                # Generar token JWT
                token = Helpers.generate_jwt(userLoginS.data)

                # Respuesta positiva
                dataRespose = {
                    "status": "success",
                    "user": userLoginS.data,
                    "token": token
                }

            else:
                dataRespose = {
                    "status": "error",
                    "message": "El password es incorrecto"
                }


        else:
            dataRespose = {
                "status": "error",
                "message": "Faltan datos por enviar"
            }

        # Devolver respuesta positiva  
        return JsonResponse({
            "status": "success",
            "accion": "Login",
            "data": dataRespose
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })

@csrf_exempt
def profile(request, id):
    if request.method == "GET":

        if id:
            try:
                user = User.objects.get(id=id)
                userS = UserSerializer(user, many=False)
                
                data = {
                    "status": "success",
                    "user": userS.data
                }

            except Exception as e:
                data = {
                    "status": "error",
                    "accion": "Error al sacar al usuario de la bd"
                }                
        else:
            data = {
                "status": "error",
                "message": "El Id no a llegado" 
            }
        
    else:
        data = {
            "status": "error",
            "message": "El metodo http es incorrecto" 
        }
    
    return JsonResponse(data)
