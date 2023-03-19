from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .utils import validate_username, validate_year

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = [
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER)
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        validators=[validate_username],
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Первое имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=255,
        choices=ROLES,
        default=USER,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default=''
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        max_length=255,
        verbose_name='Отзыв'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review')
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True, null=True
    )
    text = models.TextField(
        max_length=255,
        verbose_name='Коментарий'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Произведение'
    )
    description = models.TextField(verbose_name='Описание')
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )

    def __str__(self):
        return self.name
