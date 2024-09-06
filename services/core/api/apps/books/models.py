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
    publisher = models.CharField(_("publisher"), max_length=100)
    category = models.CharField(_("category"), max_length=100)

    @property
    def is_available(self):
        last_request = self.borrow_requests.last()
        return last_request.return_date() <= timezone.now().date()


class BookBorrowRequest(BaseModel):
    user = models.ForeignKey("users.User", related_name="borrow_requests", null=True, blank=True, on_delete=models.SET_NULL)
    book = models.ForeignKey("books.Book", related_name="borrow_requests", null=True, blank=True, on_delete=models.SET_NULL)
    period = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)

    @property
    def return_date(self):
        return self.request_date + datetime.timedelta(self.period)