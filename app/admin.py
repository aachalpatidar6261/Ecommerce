from django.contrib import admin
from .models import User,Contact, Product

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Product)
