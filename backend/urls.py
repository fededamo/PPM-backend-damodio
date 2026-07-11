from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('<int:pk>/register/', views.register_event, name='event_register'),
    path('<int:pk>/unregister/', views.unregister_event, name='event_unregister'),
]
