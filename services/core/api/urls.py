
from django.urls import path, include

urlpatterns = [
   path('api/users/', include("api.apps.users.urls")),
   path('api/books/', include("api.apps.books.urls")),
]

