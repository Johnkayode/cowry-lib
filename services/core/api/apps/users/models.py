from django.db import models
from django.utils.translation import gettext_lazy as _
from api.apps.base.models import BaseModel


class User(BaseModel):
    first_name = models.CharField(_("first name"),
        max_length=100,
        blank=False,
        null=True,
    )
    last_name = models.CharField(_("last name"),
        max_length=100,
        blank=False,
        null=True,
    )
    email = models.CharField(_("email address"), max_length=50, unique=True, blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.email
    
    