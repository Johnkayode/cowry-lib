from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    def get_deleted_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)
    
    def get_all_queryset(self):
        return super().get_queryset()