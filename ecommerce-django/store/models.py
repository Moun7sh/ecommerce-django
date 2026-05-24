from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
from decimal import Decimal

#This function creates a URL slug and appends part of a UUID if the slug already exists so we don’t get duplicates.
def _unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    Simple helper to create a (likely) unique slug by appending a short uuid
    when a slug collision occurs. Not perfect for race conditions, but OK for
    most admin workflows.
    """
    slug = slugify(value)
    ModelClass = instance.__class__
    if queryset is None:
        queryset = ModelClass.objects.all()
    slug_field = slug_field_name

    unique_slug = slug
    while queryset.filter(**{slug_field: unique_slug}).exclude(pk=getattr(instance, 'pk', None)).exists():
        unique_slug = f"{slug}{slug_separator}{uuid.uuid4().hex[:8]}"
    return unique_slug


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            # ensure slug uniqueness
            self.slug = _unique_slugify(self, self.name, slug_field_name='slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', 'title')

    def save(self, *args, **kwargs):
        if not self.slug:
            # make slug based on title and avoid collisions
            self.slug = _unique_slugify(self, self.title, slug_field_name='slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id} - {self.full_name}'

    def get_total_cost(self):
        """
        Sum of price * quantity for all order items.
        Returns Decimal('0.00') if no items.
        """
        items = self.items.all()
        total = Decimal('0.00')
        for item in items:
            total += item.get_cost()
        return total

    def items_count(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        # product may be null if the product was removed later
        product_title = getattr(self.product, 'title', 'Deleted product')
        return f'{self.quantity} x {product_title}'

    def get_cost(self):
        """
        Return total cost for this item (price * quantity) as Decimal.
        """
        try:
            return (self.price or Decimal('0.00')) * Decimal(self.quantity)
        except Exception:
            return Decimal('0.00')
