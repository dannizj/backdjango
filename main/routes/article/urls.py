from django.urls import path
from main.controllers import article

urlpatterns = [
    path('create', article.save, name="create"),
    path('article/<str:id>', article.getArticle, name="get_article"),    
    path('articles/<int:page>', article.getArticles, name="get_articles"),    
    path('delete/<str:id>', article.delete, name="delete_article"),    
    path('articles-by-user/<int:userId>', article.getArticlesByUser, name="get_article_by_user")

]