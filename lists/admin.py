from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    list_display = ("name", "user", "count_rooms")

    search_fields = ("name",)  # 검색 창

    filter_horiaontal = ("rooms",)
