from django.urls import include, path

from apps.account.views import ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include('django_registration.backends.activation.urls')),
    path('', include('django.contrib.auth.urls')),
]
