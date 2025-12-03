from django.urls import path
from .views import schedule_view, book_class, cancel_booking

urlpatterns = [
    path("", schedule_view, name="schedule"),
    path("book/<int:class_id>/", book_class, name="book_class"),
    path("cancel/<int:booking_id>/", cancel_booking, name="cancel_booking"),
]
