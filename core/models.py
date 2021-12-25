from django.db import models


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)  # model 생성 시간 자동 입력
    updated = models.DateTimeField(auto_now=True)  # model 업데이트 시간 자동 입력

    class Meta:
        abstract = True  # 추상 > DB에 반영X
