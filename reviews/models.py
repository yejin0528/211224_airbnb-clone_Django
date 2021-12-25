from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    review = models.TextField()
    accurancy = models.IntegerField()
    communication = models.IntegerField()
    cleanlines = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.review

    # return self.room.country 이런식으로도 가능!
    # return f"{self.review} - {self.room.name}"
