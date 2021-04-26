from django.contrib import admin

from .models import Category, Product, ProductReview

from django.forms import TextInput, Textarea
from django.db import models

# class YourModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':100})},
#     }

admin.site.register(ProductReview)
admin.site.register(Category)
admin.site.register(Product)
# admin.site.register(ProductReview)