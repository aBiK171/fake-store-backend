from django.urls import path
from .views import signup, profile, cart, favorites

urlpatterns = [
    path('signup/', signup),
    path('profile/', profile),
    path('cart/', cart),
    path('favorites/', favorites)
]
