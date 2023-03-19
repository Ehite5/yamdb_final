from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from reviews.models import User, Category, Genre, Title, Review, Comment
from reviews.utils import validate_username


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio',
                  'role')
        validators = [UniqueTogetherValidator(
                      queryset=User.objects.all(),
                      fields=("email",),
                      message="Данная почта уже числится в БД",),
                      validate_username]


class UserAuthorSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio',
                  'role', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [validate_username]


class TokenGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('__all__')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        model = Title
        fields = ('__all__')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        review = Review.objects.filter(author=user, title=title).exists()
        if review:
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )
        return data

    class Meta:
        fields = ('__all__')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('__all__')
        model = Comment
