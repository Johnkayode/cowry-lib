import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from api.apps.base.managers import BaseManager


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    deleted_at = models.DateTimeField(_("deleted"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
   

    objects = BaseManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        ''' soft delete objects '''
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "is_active", "updated_at"])

    def restore(self):
        ''' restore soft-deleted object '''
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "is_active", "updated_at"])