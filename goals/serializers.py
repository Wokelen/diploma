from typing import Tuple

from rest_framework import serializers, exceptions
from django.db import models, transaction

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:

        model: models.Model = GoalCategory
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")

    def validate_board(self, value: Board) -> Board:

        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted board")

        try:
            _user: BoardParticipant = BoardParticipant.objects.get(user=self.context["request"].user, board=value.id)

        except BoardParticipant.DoesNotExist:
            raise serializers.ValidationError("only users with the owner or writers role can create categories")

        if _user.role not in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            raise serializers.ValidationError("only users with the owner or writers role can create categories")

        return value


class GoalCategorySerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:

        model: models.Model = GoalCategory
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:

        model: models.Model = Goal
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")
        fields: str = "__all__"

    def validate_category(self, value: GoalCategory) -> GoalCategory:

        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        try:
            _user: BoardParticipant = BoardParticipant.objects.get(user=self.context["request"].user, board=value.board)

        except BoardParticipant.DoesNotExist:
            raise exceptions.PermissionDenied("The user can create goals only in those categories in which "
                                              "he is a member of the boards with the role of Owner or Editor")

        if _user.role not in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            raise exceptions.PermissionDenied("The user can create goals only in those categories in which "
                                              "he is a member of the boards with the role of Owner or Editor")

        return value


class GoalSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:

        model: models.Model = Goal
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:

        model: models.Model = GoalComment
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")
        fields: str = "__all__"

    def validate_goal(self, value: Goal) -> Goal:

        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted goal")

        try:
            _user = BoardParticipant.objects.get(user=self.context["request"].user, board__categories=value.category)
        except BoardParticipant.DoesNotExist:
            raise serializers.ValidationError("The user can create comments only for those goals in which "
                                              "he is a member of the boards with the role of Owner or Editor")

        if _user.role not in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            raise serializers.ValidationError("The user can create comments only for those goals in which "
                                              "he is a member of the boards with the role of Owner or Editor")

        return value


class GoalCommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:

        model: models.Model = GoalComment
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")


class BoardCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:

        model: models.Model = Board
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated")
        fields: str = "__all__"

    def create(self, validated_data: dict) -> Board:

        user: User = validated_data.pop("user")
        board: Board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:

        model: models.Model = BoardParticipant
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):

    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:

        model: models.Model = Board
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:

        owner: User = validated_data.pop("user")
        new_participants: list = validated_data.pop("participants")
        new_by_id: dict = {part["user"].id: part for part in new_participants}

        old_participants: list = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])

            instance.title = validated_data["title"]
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):

    class Meta:

        model: models.Model = Board
        fields: str = "__all__"
