from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import User
from main.models import Article
from main.validator import ArticleValidatorForm
from main.serializers import ArticleSerializer
from django.core.paginator import Paginator
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
def getArticles(request, page):
    if request.method == "GET":

        itemsPerPage = 5
    
        try:
            allArticle = Article.objects.all()
            paginator = Paginator(allArticle, itemsPerPage)
            articlesPerPage = paginator.page(page)
            pageObj = paginator.get_page(page)

            articles = ArticleSerializer(articlesPerPage, many=True)
    
            dataResponse ={
                "status": "success",
                "articles": articles.data,
                "itemsPerPage": itemsPerPage,
                "pages": pageObj.paginator.num_pages,
                "totalArticles": len(allArticle)
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
def delete(request, id):
    if request.method == "DELETE":
    
        try:
            article = Article.objects.get(id=id)
            article.delete()
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
def getArticlesByUser(request, userId):
    if request.method == "GET":

        articles = Article.objects.filter( user = userId)
        articlesS = ArticleSerializer(articles, many=True)

        data = {
            "status": "success",
            "articles": articlesS.data
        }
    else:
        data ={
            "status": "error",
            "message": "El metodo http es incorrecto" 
        }

    return JsonResponse(data)
