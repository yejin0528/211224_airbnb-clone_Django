from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80, default="")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Amenity(AbstractItem):
    pass

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    pass

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    pass

    class Meta:
        verbose_name = "House Rule"  # 뒤에 s는 유지: House Rules


class RoomType(AbstractItem):
    pass

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]  # 이름순 정렬


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )  # 참조키, 1대다
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # override
        self.city = str.capitalize(self.city)  # 첫글자 대문자로!
        super().save(*args, **kwargs)

    # override
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rate(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()

        if len(all_reviews) == 0:
            return 0
        else:
            return all_ratings / len(all_reviews)


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")  # uploads의 어떤 폴더에 업로드 할 것인지
    room = models.ForeignKey(
        Room, related_name="photos", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.caption
