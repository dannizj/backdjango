from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Article

@csrf_exempt
def save(request):
    if request.method == "POST":
        nombre = "Dani zj web"

        return JsonResponse({
            "status": "success",
            "nombre": nombre
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })

@csrf_exempt
def getArticles(request):
    if request.method == "POST":
        nombre = "Dani zj web"

        return JsonResponse({
            "status": "success",
            "accion": "Get Articles"
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })

@csrf_exempt
def getArticle(request):
    if request.method == "POST":
        nombre = "Dani zj web"

        return JsonResponse({
            "status": "success",
            "accion": "Get Article"
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })

@csrf_exempt
def delete(request):
    if request.method == "POST":
        nombre = "Dani zj web"

        return JsonResponse({
            "status": "success",
            "accion": "Delete Article"
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })

@csrf_exempt
def getArticleByUser(request):
    if request.method == "POST":
        nombre = "Dani zj web"

        return JsonResponse({
            "status": "success",
            "accion": "Get Article By User"
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "El metodo http es incorrecto" 
        })
