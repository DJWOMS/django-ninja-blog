from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """Класс модели категорий сетей"""
    name = models.CharField("Категория", max_length=50)
    published = models.BooleanField("Опубликовать?", default=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Класс модели тегов"""
    name = models.CharField("Тег", max_length=50, unique=True, null=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Post(models.Model):
    """Класс модели поста"""
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE)
    title = models.CharField("Тема", max_length=500)
    mini_text = models.TextField("Краткое содержание", max_length=5000)
    text = models.TextField("Полное содержание", max_length=10000000)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    published_date = models.DateTimeField(
        "Дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField("Изображение", upload_to="blog/", blank=True)
    tag = models.ManyToManyField(Tag, verbose_name="Тег", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    published = models.BooleanField("Опубликовать?", default=True)
    viewed = models.IntegerField("Просмотрено", default=0)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_date"]

    def get_category_description(self):
        return self.category.description

    def get_count_comments(self):
        return f"{self.comments.all().count()}"

    def get_comments(self):
        return self.comments.filter(parent=None)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель коментариев к новостям"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, verbose_name="Новость", related_name="comments", on_delete=models.CASCADE
    )
    text = models.TextField("Сообщение", default='')
    parent = models.ForeignKey(
        "self",
        verbose_name="Родительский комментарий",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return "{} - {}".format(self.user, self.post)

