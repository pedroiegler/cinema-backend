from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'genres', views.GenreViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'ratings', views.RatingViewSet, basename='rating')
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]