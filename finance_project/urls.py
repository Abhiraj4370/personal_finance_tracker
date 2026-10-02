from django.contrib import admin
from django.urls import path, include
from transactions.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('transactions.urls')),
    path('dashboard/', dashboard, name='dashboard'),
])
