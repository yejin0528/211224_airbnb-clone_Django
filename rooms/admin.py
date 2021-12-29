from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):  # admin안에 admin 가능
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Space", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 접기 더보기
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rate",  # def total_rate
    )

    raw_id_fields = ("host",)

    # ordering = ("name", "price")  # 정렬

    list_filter = ("instant_book", "city", "country")

    search_fields = ("=city", "^host__username")  # 검색창 , relationship(__), startwith(^)

    filter_horizontal = (  # ManytoMany
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):  # obj: row
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()  # related_name = "photos"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumnail")

    def get_thumnail(self, obj):
        return mark_safe(f"<img width='50px'src='{obj.file.url}' />")

    get_thumnail.short_description = "Thumnail"
