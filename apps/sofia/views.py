from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from django.db.models.functions import Trunc
from django.db.models import Q, Sum, IntegerField, Value, Count
from django import template

import datetime
import calendar

from .serializers import OrderSerializer

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response


@csrf_exempt
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class SalesState(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        states = []
        count = []
        sales = Order.objects.values('state').annotate(dcount=Count('state')).order_by('-dcount')[:6]

        for state in sales:
            states.append(state['state'])
            count.append(state['dcount'])

        data = {
            'state': states,
            'count': count,
        }
        return Response(data)


class TotalShipments(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        shipmonth = []
        ship = []
        totalship = Order.objects.annotate(sales_date=Trunc('created_at', 'month')).values('sales_date').annotate(
            sales=Count('paid_amount')).order_by('-sales_date')[:6]
        totalship = reversed(totalship)

        for month in totalship:
            shipmonth.append(calendar.month_name[month['sales_date'].month])
            ship.append(month['sales'])

        data = {
            'ship': ship,
            'month': shipmonth,
        }
        return Response(data)


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
    orders = Order.objects.all().order_by('-created_at')[:7]

    todaysales = Order.objects.annotate(sales_date=Trunc('created_at', 'day')).values('sales_date').annotate(
        sales=Sum('paid_amount')).order_by('-sales_date')[:1]
    for sales in todaysales:
        currsales = sales['sales']

    totalship = Order.objects.all().count()

    context = {}
    context['segment'] = 'index'
    context['orders'] = orders
    context['dailysales'] = currsales
    context['totalship'] = totalship

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))
