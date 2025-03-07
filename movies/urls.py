from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('friends.urls')),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('new/', views.add_new, name='add-new'),
]
