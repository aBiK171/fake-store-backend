from django.contrib import admin
from .models import CartItem
from .models import Favorite

admin.site.register(CartItem)
admin.site.register(Favorite)
