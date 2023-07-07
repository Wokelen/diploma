from typing import Tuple

from django.contrib import admin

from bot.models import TgUser


class TgUserAdmin(admin.ModelAdmin):
    """
    The TgUserAdmin class inherits from the ModelAdmin class. Defines the output of instance fields
    to the administration panel and the ability to edit them.
    """
    list_display: Tuple[str] = ("chat_id", "user", "verification_code")
    readonly_fields: Tuple[str] = ("chat_id", "verification_code")
    search_fields: Tuple[str] = ("user", "chat_id")


admin.site.register(TgUser, TgUserAdmin)
