from django.urls import path
from api.apps.users import views


urlpatterns = [
    path("enrol/", views.EnrolUserView.as_view(), name="enrol_user"),
]