from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # смена языка
    path('i18n/', include('django.conf.urls.i18n')),

    # авторизация и кабинет
    path('user/', include('apps.users.urls')),

    # админка
    path('admin/', admin.site.urls),

    # главная страница и прочие
    path('', include('apps.pages.urls')),

    path("schedule/", include("apps.schedule.urls")),

    path('bookings/', include('apps.bookings.urls')),

    path('memberships/', include('apps.membership.urls')),

]
