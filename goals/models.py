from typing import List, Tuple

from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):

    class Meta:

        abstract: bool = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):

        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Board(DatesModelMixin):

    class Meta:

        verbose_name: str = "Доска"
        verbose_name_plural: str = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):

    class Meta:

        unique_together: Tuple[str, ...] = ("board", "user")
        verbose_name: str = "Участник"
        verbose_name_plural: str = "Участники"

    class Role(models.IntegerChoices):

        owner: Tuple[int, str] = 1, "Владелец"
        writer: Tuple[int, str] = 2, "Редактор"
        reader: Tuple[int, str] = 3, "Читатель"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="participants")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="participants")
    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.owner)


class GoalCategory(DatesModelMixin):

    class Meta:

        verbose_name: str = "Категория"
        verbose_name_plural: str = "Категории"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Название", max_length=255)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin):

    class Meta:

        verbose_name: str = "Цель"
        verbose_name_plural: str = "Цели"

    class Status(models.IntegerChoices):

        to_do: Tuple[int, str] = 1, "К выполнению"
        in_progress: Tuple[int, str] = 2, "В процессе"
        done: Tuple[int, str] = 3, "Выполнено"
        archived: Tuple[int, str] = 4, "Архив"

    class Priority(models.IntegerChoices):

        low: Tuple[int, str] = 1, "Низкий"
        medium: Tuple[int, str] = 2, "Средний"
        high: Tuple[int, str] = 3, "Высокий"
        critical: Tuple[int, str] = 4, "Критический"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    due_date = models.DateField(verbose_name="Дата дедлайна", null=True)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class GoalComment(DatesModelMixin):

    class Meta:

        verbose_name: str = "Комментарий"
        verbose_name_plural: str = "Комментарии"
        ordering: List[str] = ["-created"]

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name="Цель")