from django.db import models
from django.db.models.fields import related
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():  # Querty Set
            usernames.append(user.username)
        return ", ".join(usernames)  # join > 배열을 String형으로 바꾸기 위해

    def count_messages(self):
        return self.messages.count()  # related_name="messages"

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()  # related_name="messages"

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} say: {self.message}"
