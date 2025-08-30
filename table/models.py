from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['name', 'transaction_type']

    def __str__(self):
        return f"{self.name}"

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.name}"

class FinancialTransaction(models.Model):
    created_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date', '-id']
    
    def __str__(self):
        return f"{self.created_date} - {self.amount} руб."
    