from django.db import models


class Product(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pk']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name