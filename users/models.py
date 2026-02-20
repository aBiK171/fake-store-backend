from django.contrib.auth.models import User
from django.db import models


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product_id}"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product_id')
