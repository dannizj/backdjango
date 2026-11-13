from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import User
from main.models import Article
from main.validator import ArticleValidatorForm
from main.serializers import ArticleSerializer
import json

@csrf_exempt
def save(request):
    if request.method == "POST":

        data = json.loads(request.body)
        title = data.get("title", "")
        content = data.get("content", "")

        if data and title and content:
            user = User.objects.get(id=request.user['id'])

            form = ArticleValidatorForm(data)

            if form.is_valid():
                article = Article(
                    title = title,
                    content = content,
                    user= user
                )
            else:
                dataResponse = {
                    "statur": "error",
                    "message": "Error en la validacion de datos"
                }

            try:
                article.save()
                articleS = ArticleSerializer(article, many=False)
                dataResponse = {
                    "status": "success",
                    "article": articleS.data
                }
            except Exception as e:
                dataResponse = {
                    "statur": "error",
                    "message": "Error en la validacion de datos"
                }
        else:
            dataResponse = {
                "statur": "error",
                "message": "Error en el envio de datos"
            }

    else:
        dataResponse = {
            "status": "error",
            "message": "El metodo http es incorrecto" 
        }
    
    return JsonResponse(dataResponse)


@csrf_exempt
def getArticle(request, id):
    if request.method == "GET":

        try:
            article = Article.objects.get(id=id)
            articleS = ArticleSerializer(article, many=False)

            dataResponse ={
                "status": "success",
                "article": articleS.data
            }

        except Exception as e:
            dataResponse ={
                "status": "error",
                "message": str(e)
            }

    else:
        dataResponse ={
            "status": "error",
            "message": "El metodo http es incorrecto" 
        }
    return JsonResponse(dataResponse)

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
