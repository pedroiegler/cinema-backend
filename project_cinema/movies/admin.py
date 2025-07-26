from django.contrib import admin
from .models import Genre, Movie, Rating, Comment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ['user', 'created_at']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['user', 'created_at']
    fields = ['user', 'content', 'is_active', 'created_at']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'duration', 'release_date', 'average_rating', 'total_ratings', 'is_active']
    list_filter = ['genres', 'release_date', 'is_active']
    search_fields = ['title', 'director', 'cast']
    filter_horizontal = ['genres']
    date_hierarchy = 'release_date'
    ordering = ['-release_date']
    inlines = [RatingInline, CommentInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'synopsis')
        }),
        ('Detalhes', {
            'fields': ('duration', 'release_date', 'director', 'cast')
        }),
        ('Mídia', {
            'fields': ('poster', 'trailer_url')
        }),
        ('Categorização', {
            'fields': ('genres', 'is_active')
        }),
    )
    
    def average_rating(self, obj):
        avg = obj.average_rating
        return f"{avg:.1f}" if avg else "Sem avaliações"
    average_rating.short_description = "Média"
    
    def total_ratings(self, obj):
        return obj.total_ratings
    total_ratings.short_description = "Total de avaliações"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'movie']
    search_fields = ['movie__title', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'content_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'movie']
    search_fields = ['movie__title', 'user__username', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Conteúdo"