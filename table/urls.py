from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('update/<int:pk>/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('delete/<int:pk>/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('reference-books/', views.ReferenceBooksView.as_view(), name='reference_books'),
    path('reference-books/add-status/', views.add_status, name='add_status'),
    path('reference-books/edit-status/', views.edit_status, name='edit_status'),
    path('reference-books/delete-status/<int:pk>/', views.delete_status, name='delete_status'),
    path('reference-books/add-type/', views.add_type, name='add_type'),
    path('reference-books/edit-type/', views.edit_type, name='edit_type'),
    path('reference-books/delete-type/<int:pk>/', views.delete_type, name='delete_type'),
    path('reference-books/add-category/', views.add_category, name='add_category'),
    path('reference-books/edit-category/', views.edit_category, name='edit_category'),
    path('reference-books/delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('reference-books/add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('reference-books/edit-subcategory/', views.edit_subcategory, name='edit_subcategory'),
    path('reference-books/delete-subcategory/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
    path('load-categories/', views.load_categories, name='load_categories'),
    path('load-subcategories/', views.load_subcategories, name='load_subcategories'),
    path('delete-status/<int:pk>/', views.delete_status, name='delete_status'),
]
