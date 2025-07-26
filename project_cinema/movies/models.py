from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Movie(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duração em minutos")
    release_date = models.DateField()
    director = models.CharField(max_length=200)
    cast = models.TextField(help_text="Elenco principal")
    poster = models.ImageField(upload_to='posters/', blank=True)
    trailer_url = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        """Calcula a média das avaliações"""
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return None
    
    @property
    def total_ratings(self):
        """Total de avaliações"""
        return self.ratings.count()
    
    class Meta:
        ordering = ['-release_date']


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/5)"
    
    class Meta:
        unique_together = ['movie', 'user']  # Um usuário só pode avaliar um filme uma vez
        ordering = ['-created_at']


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
    class Meta:
        ordering = ['-created_at']
    