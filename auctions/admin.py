from django.contrib import admin

from .models import Category, Product, Bid, Comment, Watchlist

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = { 'slug': ('name',) }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'description', 'starting_bid',
        'created', 'updated', 'is_active',
        'slug'
        ]

    list_filter = ['is_active']
    list_editable = ['starting_bid', 'is_active']
    prepopulated_fields = { 'slug': ('title',) }

"""
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_time', 'bid_amount']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'created_on']

"""

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)