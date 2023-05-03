from django.db import models
from rest_framework import status
from common_config.utils import APIResponse
from common_config.message import INSTANCE_DELETION_SUCCESS


# Create your models here.
class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """
    Base model for other models holding common details
    """
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    def delete(self, archive=False):
        if archive:
            self.is_deleted = True
            self.save()
        else:
            super(BaseModel, self).delete()
        return APIResponse({}, status=status.HTTP_200_OK, custom_message=INSTANCE_DELETION_SUCCESS)
