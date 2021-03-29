from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Order
from django.db.models.functions import Trunc
from django.db.models import Q, Sum, IntegerField, Value, Count
from django import template

import datetime
import calendar

from rest_framework.views import APIView
from rest_framework.response import Response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        month = []
        value = []
        orders = []

        queryset = Order.objects.annotate(sales_date=Trunc('created_at', 'month')).values('sales_date').annotate(
            sales=Sum('paid_amount')).order_by('-sales_date')[:12]
        queryset = reversed(queryset)

        queryset2 = Order.objects.annotate(sales_date=Trunc('created_at', 'month')).values('sales_date').annotate(
            sales=Count('paid_amount')).order_by('-sales_date')[:12]
        queryset2 = reversed(queryset2)

        for order in queryset2:
            orders.append(order['sales'])

        for sales in queryset:
            month.append(calendar.month_name[sales['sales_date'].month])
            value.append(sales['sales'])

        data = {
            'month': month,
            'sales': value,
            'order': orders,
        }
        return Response(data)


def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))
