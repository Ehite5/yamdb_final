from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework import filters, status, viewsets, mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import (SignUpSerializer, TokenGetSerializer,
                             CategorySerializer, UserAuthorSerializer,
                             UserSerializer, GenreSerializer,
                             TitleSerializer, TitlesSerializer,
                             ReviewSerializer, CommentsSerializer)
from api.permissions import (IsAdminOnly, AdminOrReadOnlyPermission,
                             ReviewCommentsPermission)
from reviews.models import User, Category, Genre, Title
from .filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = UserAuthorSerializer(request.user,
                                              data=request.data,
                                              partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def send_code(request):
    """Получение кода подтверждения на почту для регистрации на проекте."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
    )
    token = default_token_generator.make_token(user)
    user.token = token
    user.save()
    send_mail(
        'Регистрация пользователя',
        (f'Вы получили код подтверждения регистрации на почтовый адрес.\n'
            f'Почта: {user.email}\n' f'Код подтверждения: {user.token}'),
        f'{settings.EMAIL_FROM}',
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    """Получение JWT-токена при передаче username и confirmation code."""
    serializer = TokenGetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if serializer.validated_data.get(
            'confirmation_code') == user.confirmation_code:
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)},
                        status=status.HTTP_201_CREATED)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [AdminOrReadOnlyPermission]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlesSerializer
        return TitleSerializer


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [AdminOrReadOnlyPermission]
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnlyPermission,)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentsPermission, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [ReviewCommentsPermission, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
