from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/category_update/', views.LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign_agent/', views.LeadAssigneAgentView.as_view(), name='lead-assign_agent'),
    path('create/', views.LeadCreateView.as_view(), name='lead-create'),
]