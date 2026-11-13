from django.urls import path
from main.controllers import article

urlpatterns = [
    path('create', article.save, name="create"),
    path('articles/<int:page>', article.getArticles, name="get_articles"),    
    path('article/<str:id>', article.getArticle, name="get_article"),    
    path('delete/<str:id>', article.delete, name="delete_article"),    
    path('article-by-user/<int:userId>', article.getArticleByUser, name="get_article_by_user")

]