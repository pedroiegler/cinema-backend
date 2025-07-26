from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Genre, Movie, Rating, Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'user', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'movie', 'user', 'content', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        source='genres'
    )
    average_rating = serializers.ReadOnlyField()
    total_ratings = serializers.ReadOnlyField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'synopsis', 'duration',
            'release_date', 'director', 'cast', 'poster', 'trailer_url',
            'genres', 'genre_ids', 'is_active', 'created_at', 'updated_at',
            'average_rating', 'total_ratings', 'user_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_user_rating(self, obj):
        """Retorna a avaliação do usuário atual para este filme"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = obj.ratings.get(user=request.user)
                return rating.rating
            except Rating.DoesNotExist:
                return None
        return None


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    genres = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_ratings = serializers.ReadOnlyField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'duration', 'release_date', 'poster',
            'genres', 'is_active', 'average_rating', 'total_ratings'
        ]


class MovieDetailSerializer(MovieSerializer):
    """Serializer detalhado com comentários"""
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['comments', 'comments_count']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_active=True).count()