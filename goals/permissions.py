from rest_framework import permissions

from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Board) -> bool:

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()

        return BoardParticipant.objects.filter(user=request.user, board=obj,
                                               role=BoardParticipant.Role.owner).exists()


class CategoryPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: GoalCategory) -> bool:

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()

        else:
            _user = BoardParticipant.objects.filter(user=request.user, board=obj.board).get()
            return _user.role in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]


class GoalPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: Goal) -> bool:

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board__categories=obj.category).exists()

        _user = BoardParticipant.objects.get(user=request.user, board__categories=obj.category)
        return _user.role in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]


class CommentPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: GoalComment) -> bool:

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board__category__goal=obj.goal).exists()

        return obj.user == request.user
