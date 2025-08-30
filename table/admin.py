from django.contrib import admin
from .models import Status, TransactionType, \
    Category, Subcategory, FinancialTransaction

# Register your models here.
admin.site.register(Status)
admin.site.register(TransactionType)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(FinancialTransaction)
