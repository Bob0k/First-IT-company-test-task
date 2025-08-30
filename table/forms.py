from datetime import date

from django import forms
from .models import FinancialTransaction, Status, TransactionType, Category, Subcategory

class FinancialTransactionForm(forms.ModelForm):
    class Meta:
        model = FinancialTransaction
        fields = '__all__'
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_transaction_type'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'created_date': 'Дата создания',
            'status': 'Статус',
            'transaction_type': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма',
            'comment': 'Комментарий'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created_date'].initial = date.today()

        # Dymanic update of queryset for categories
        if 'transaction_type' in self.data:
            try:
                transaction_type_id = int(self.data.get('transaction_type'))
                self.fields['category'].queryset = Category.objects.filter(
                    transaction_type_id=transaction_type_id
                )
            except (ValueError, TypeError):
                pass

        # Dymanic update of queryset for subcategories
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
            