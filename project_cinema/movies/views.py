from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Genre, Movie, Rating, Comment
from .serializers import (
    GenreSerializer, MovieSerializer, MovieListSerializer, MovieDetailSerializer,
    RatingSerializer, CommentSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'release_date']
    search_fields = ['title', 'director', 'cast']
    ordering_fields = ['title', 'release_date']
    ordering = ['-release_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer
    
    @action(detail=False, methods=['GET'])
    def top_rated(self, request):
        """Filmes mais bem avaliados"""
        movies = Movie.objects.filter(is_active=True, ratings__isnull=False).distinct()
        # Ordenar por média de avaliação (calculada no Python por simplicidade)
        movies = sorted(movies, key=lambda x: x.average_rating or 0, reverse=True)[:10]
        
        serializer = MovieListSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def recent(self, request):
        """Filmes recentes"""
        recent_movies = Movie.objects.filter(
            is_active=True,
            release_date__lte=timezone.now().date()
        ).order_by('-release_date')[:10]
        
        serializer = MovieListSerializer(recent_movies, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def coming_soon(self, request):
        """Filmes em breve"""
        coming_movies = Movie.objects.filter(
            is_active=True,
            release_date__gt=timezone.now().date()
        ).order_by('release_date')[:10]
        
        serializer = MovieListSerializer(coming_movies, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def rate(self, request, pk=None):
        """Avaliar um filme"""
        movie = self.get_object()
        rating_value = request.data.get('rating')
        
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response(
                {'error': 'Rating deve ser um número entre 1 e 5'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating, created = Rating.objects.update_or_create(
            movie=movie,
            user=request.user,
            defaults={'rating': rating_value}
        )
        
        serializer = RatingSerializer(rating, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=True, methods=['DELETE'])
    def remove_rating(self, request, pk=None):
        """Remover avaliação de um filme"""
        movie = self.get_object()
        try:
            rating = Rating.objects.get(movie=movie, user=request.user)
            rating.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response(
                {'error': 'Você não avaliou este filme'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['movie', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['movie']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # Só permite editar próprios comentários
        if serializer.instance.user != self.request.user:
            return Response(
                {'error': 'Você só pode editar seus próprios comentários'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()