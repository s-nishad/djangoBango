from django.db import models

# Create your models here.
from core.utils import guid_factory


class BlankModel(models.Model):

    class Meta:
        abstract = True


class AbstractBaseModel(BlankModel):
    guid = models.CharField(max_length=255, default=guid_factory, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Row {self.guid}'


class ApiKey(AbstractBaseModel):
    host = models.URLField(null=True, blank=True)
    service_name = models.CharField(max_length=100)
    secret = models.CharField(max_length=32, default=guid_factory, db_index=True)
