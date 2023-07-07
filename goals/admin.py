
from django.contrib import admin

from goals.models import GoalCategory, GoalComment, Goal, BoardParticipant, Board


class ParticipantsInline(admin.TabularInline):
    model = BoardParticipant
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(role=BoardParticipant.Role.owner)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_deleted')
    list_display_links = ['title']
    list_filter = ['is_deleted']
    search_fields = ['title']
    inlines = [ParticipantsInline]


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('created', 'updated')
    list_filter = ['is_deleted']
    search_fields = ['title']


class CommentsInline(admin.StackedInline):
    model = GoalComment
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    readonly_fields = ('created', 'updated')
    list_filter = ['status', 'priority']
    search_fields = ['title', 'description']
    inlines = [CommentsInline]


