import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from api.apps.base.models import BaseModel


class Book(BaseModel):
    title = models.CharField(_("title"),
        max_length=100,
        blank=False,
        null=False,
    )
    author = models.CharField(_("author"), max_length=100)
    publisher = models.CharField(_("publisher"), max_length=100)
    category = models.CharField(_("category"), max_length=100)

    @property
    def is_unavailable(self):
        last_request = self.borrow_requests.first()
        if last_request:
            return last_request.return_date > timezone.now().date()
        return False

    class Meta:
        ordering = ("-created_at",)
    
    @classmethod
    def available_books(cls):
        now = timezone.now().date()
        return cls.objects.annotate(
            is_available=models.Case(
                models.When(
                    borrow_requests__isnull=True,
                    then=models.Value(True),
                ),
                models.When(
                    borrow_requests__return_date__lte=now,
                    then=models.Value(True),
                ),
                default=models.Value(False),
                output_field=models.BooleanField(),
            )
        ).filter(is_available=True).distinct()


class BookBorrowRequest(BaseModel):
    user = models.ForeignKey("users.User", related_name="borrow_requests", null=True, blank=True, on_delete=models.SET_NULL)
    book = models.ForeignKey("books.Book", related_name="borrow_requests", null=True, blank=True, on_delete=models.SET_NULL)
    period = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.return_date:
            self.return_date = self.request_date + datetime.timedelta(days=self.period)
            self.save()