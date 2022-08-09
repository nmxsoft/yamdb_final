from django.utils import timezone
from rest_framework import serializers

from reviews.models import (SCORE_CHOICES, Category, Comment, Genre, Review,
                            Title)
from users.models import User


class ValidateMeMixin:
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя me зарезервировано системой.'
            )
        return value


class EmailSerializer(ValidateMeMixin, serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        max_length=150,
        required=True,
        regex=r'^[\w.@+-]',
    )


class CodeSerializer(ValidateMeMixin, serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r'^[\w.@+-]',
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(choices=SCORE_CHOICES)

    class Meta:
        model = Review
        fields = ('id', 'author', 'pub_date', 'text', 'score')

    def validate(self, data):
        title = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв этому произведению.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        current_year = timezone.now().year
        if 0 <= current_year <= value:
            raise serializers.ValidationError(
                'Проверьте год создания произведения'
                '(год выпуска должен быть н.э.).'
            )
        return value
