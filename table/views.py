from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import FinancialTransaction, Status, TransactionType, Category, Subcategory
from .forms import FinancialTransactionForm


class TransactionListView(ListView):
    model = FinancialTransaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Transaction list filtration
        status = self.request.GET.get('status')
        transaction_type = self.request.GET.get('transaction_type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        date_from = self.request.GET.get('date_from')   
        date_to = self.request.GET.get('date_to')
        
        if status:
            queryset = queryset.filter(status_id=status)
        if transaction_type:
            queryset = queryset.filter(transaction_type_id=transaction_type)
        if category:
            queryset = queryset.filter(category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)
        if date_from:
            queryset = queryset.filter(created_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_date__lte=date_to)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['transaction_types'] = TransactionType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context

class TransactionCreateView(CreateView):
    model = FinancialTransaction
    form_class = FinancialTransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('transaction_list')

class TransactionUpdateView(UpdateView):
    model = FinancialTransaction
    form_class = FinancialTransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('transaction_list')

class TransactionDeleteView(DeleteView):
    model = FinancialTransaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

# For dynamic update
def load_categories(request):
    transaction_type_id = request.GET.get('transaction_type_id')
    categories = Category.objects.filter(transaction_type_id=transaction_type_id)
    return JsonResponse(list(categories.values('id', 'name')), safe=False)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

class ReferenceBooksView(TemplateView):
    template_name = 'reference_books.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['transaction_types'] = TransactionType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context

# CRUD reference book operations
def add_status(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Status.objects.get_or_create(name=name.strip())
            messages.success(request, f'Статус "{name}" добавлен')
        return redirect('reference_books')
    
def edit_status(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        status_id = request.POST.get('status_id')
        if name and status_id:
            status = get_object_or_404(Status, pk=status_id)
            status.name = name
            status.save()
            messages.success(request, f'Статус "{name}" изменен')
        return redirect('reference_books')

def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    status.delete()
    messages.success(request, f'Статус "{status.name}" удален')
    return redirect('reference_books')

def add_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            TransactionType.objects.get_or_create(name=name.strip())
            messages.success(request, f'Тип операции "{name}" добавлен')
        return redirect('reference_books')
    
def edit_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        transaction_type_id = request.POST.get('type_id')
        if name and transaction_type_id:
            type = get_object_or_404(TransactionType, pk=transaction_type_id)
            type.name = name
            type.save()
            messages.success(request, f'Тип операции "{name}" изменен')
        return redirect('reference_books')

def delete_type(request, pk):
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    transaction_type.delete()
    messages.success(request, f'Тип операции "{transaction_type.name}" удален')
    return redirect('reference_books')

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        transaction_type_id = request.POST.get('transaction_type')
        if name and transaction_type_id:
            transaction_type = get_object_or_404(TransactionType, pk=transaction_type_id)
            Category.objects.get_or_create(
                name=name.strip(),
                transaction_type=transaction_type,
            )
            messages.success(request, f'Категория "{name}" добавлена')
        return redirect('reference_books')

def edit_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        transaction_type_id = request.POST.get('transaction_type')
        category_id = request.POST.get('category_id')
        if name and transaction_type_id and category_id:
            category = get_object_or_404(Category, pk=category_id)
            transaction_type = get_object_or_404(TransactionType, pk=transaction_type_id)
            category.name = name
            category.transaction_type = transaction_type
            category.save()
            messages.success(request, f'Категория "{name}" изменена')
        return redirect('reference_books')
    
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, f'Категория "{category.name}" удалена')
    return redirect('reference_books')

def add_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, pk=category_id)
            Subcategory.objects.get_or_create(
                name=name.strip(),
                category=category
            )
            messages.success(request, f'Подкатегория "{name}" добавлена')
        return redirect('reference_books')

def edit_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory_id')
        if name and category_id and subcategory_id:
            subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
            category = get_object_or_404(Category, pk=category_id)
            subcategory.name = name
            subcategory.category = category
            subcategory.save()
            messages.success(request, f'Категория "{name}" изменена')
        return redirect('reference_books')
    
def delete_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    subcategory.delete()
    messages.success(request, f'Подкатегория "{subcategory.name}" удалена')
    return redirect('reference_books')
