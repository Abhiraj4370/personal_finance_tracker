from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import Account, Category, Transaction
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer

def dashboard(request):
    return render(request, 'dashboard.html')

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('category', 'account')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReportsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        now = timezone.localtime(timezone.now()).date()
        year = now.year
        month = now.month

        qs = Transaction.objects.filter(
            user=user,
            date__year=year,
            date__month=month,
            category__type=Category.EXPENSE
        ).values('category__id', 'category__name', 'category__color')          .annotate(total_amount=Coalesce(Sum('amount'), 0))          .order_by('-total_amount')

        labels = []
        data = []
        colors = []
        total_sum = 0
        rows = []
        for item in qs:
            labels.append(item['category__name'])
            data.append(float(item['total_amount']))
            colors.append(item.get('category__color') or None)
            total_sum += float(item['total_amount'])
            rows.append(item)

        return Response({
            'month': f"{year}-{month:02d}",
            'labels': labels,
            'data': data,
            'colors': colors,
            'total': total_sum,
            'rows': rows
        })
