from django.db import models
from django.conf import settings


class StatDate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='statdates')
    date1 = models.DateField()
    date2 = models.DateField()

    def __str__(self):
        return f'Entre {self.date1} - {self.date2}'
