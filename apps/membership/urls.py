from django.urls import path
from .views import (
    membership_list_view,
    buy_membership_view,
    membership_success_view,
    membership_history_view,
)

urlpatterns = [
    path('', membership_list_view, name='memberships'),
    path('buy/<int:pk>/', buy_membership_view, name='buy_membership'),
    path('success/', membership_success_view, name='membership_success'),
    path('history/', membership_history_view, name='membership_history'),
]
