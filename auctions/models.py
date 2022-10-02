from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('auctions:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255)
    #number_of_bids = models.IntegerField()
    # winner = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='auction_won')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, default=None, null=True, related_name='auction_won')

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('auctions:product_detail', args=[self.slug])

    def __str__(self):
        return self.title 

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidding_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bidded_product')
    bid_time = models.DateField(auto_now=True)
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Bids'

    def __str__(self):
        return self.user

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='commented_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_commenting')
    body = models.TextField()
    created_on = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.body

class Watchlist(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_watcher')

    def __str__(self):
        return f"user:({self.user}), product:({self.product})"