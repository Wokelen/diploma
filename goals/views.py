from typing import List

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import serializers
from django.db import models, transaction

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions, CategoryPermissions, GoalPermissions
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalCategoryCreateSerializer, GoalSerializer, \
    BoardCreateSerializer, BoardSerializer, BoardListSerializer
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCategoryCreateView(CreateAPIView):

    model: models.Model = GoalCategory
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):

    model: models.Model = GoalCategory
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields: List[str] = ["title", "created"]
    ordering: List[str] = ["title"]
    filterset_fields: List[str] = ["title", "board", "user"]

    def get_queryset(self) -> list:

        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):

    model: models.Model = GoalCategory
    serializer_class: serializers.ModelSerializer = GoalCategorySerializer
    permission_classes: list = [permissions.IsAuthenticated, CategoryPermissions]

    def get_queryset(self) -> list:

        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user).exclude(is_deleted=True)


    def perform_destroy(self, instance: GoalCategory) -> None:

        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goal_set.update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):

    model: models.Model = Goal
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCreateSerializer


class GoalListView(ListAPIView):

    model: models.Model = Goal
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields: List[str] = ["title", "created"]
    ordering: List[str] = ["title"]
    search_fields: List[str] = ["title", "description"]

    def get_queryset(self) -> list:

        return Goal.objects.select_related('user').filter(
            category__board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalView(RetrieveUpdateDestroyAPIView):

    model: models.Model = Goal
    serializer_class: serializers.ModelSerializer = GoalSerializer
    permission_classes: list = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self) -> list:

        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Goal) -> None:

        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(CreateAPIView):

    model: models.Model = GoalComment
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):

    model: models.Model = GoalComment
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields: List[str] = ["text", "goal", "created", "updated"]
    filterset_fields: List[str] = ["goal"]

    def get_queryset(self) -> list:

        return GoalComment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):

    model: models.Model = GoalComment
    serializer_class: serializers.ModelSerializer = GoalCommentSerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self) -> list:

        return GoalComment.objects.filter(user=self.request.user)


class BoardCreateView(CreateAPIView):

    model: models.Model = Board
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = BoardCreateSerializer


class BoardListView(ListAPIView):

    model: models.Model = Board
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields: List[str] = ["title", ]
    filterset_fields: List[str] = ["title", ]

    def get_queryset(self) -> list:

        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):

    model: models.Model = Board
    permission_classes: list = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> List[Board]:

        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> None:

        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
