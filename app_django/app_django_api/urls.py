from django.urls import path
from . import views

urlpatterns = [
    path('posts/',views.postsList, name="posts"),
    path('stats/',views.postsStats, name="stats"),
    path('stats/<str:author>',views.postsStatsAuthors, name="stats-authors" ),
    path('authors/',views.postsAuthorsAuthor, name="authors" )
    ]