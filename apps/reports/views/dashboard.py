# Django
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime

# Django Rest Framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ValidationError

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Models
from apps.sales.models.sales import Sales
from apps.purchases.models.purchases import Purchases
from apps.sales.models.customers import Customers


class DashboardReportsViewset(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'filter_date',
                openapi.IN_QUERY,
                description="Fecha actual en formato YYYY-MM-DD",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ventas': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'total_ventas': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'compras': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'total_compras': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'utilidad': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'clientes_nuevos': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'todos_los_clientes': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        }
    )
    @action(detail=False, methods=["GET"])
    def metrics(self, request, *args, **kwargs):
        # Obtener parámetro de fecha actual
        filter_date = request.query_params.get("filter_date")
        if filter_date:
            try:
                fecha = datetime.strptime(filter_date, "%Y-%m-%d")
            except ValueError:
                raise ValidationError({'detail': ["Formato de fecha inválido. Use YYYY-MM-DD"]})
        else:
            fecha = now()

        mes_actual = fecha.month
        anno_actual = fecha.year

        # Cálculos
        ventas_mes = Sales.objects.filter(sale_date__year=anno_actual, sale_date__month=mes_actual, is_active=True)
        total_ventas = ventas_mes.aggregate(total=Sum("total"))["total"] or 0

        compras_mes = Purchases.objects.filter(purchase_date__year=anno_actual, purchase_date__month=mes_actual, is_active=True)
        total_compras = compras_mes.aggregate(total=Sum("total"))["total"] or 0

        clientes_nuevos = Customers.objects.filter(created__year=anno_actual, created__month=mes_actual, is_active=True).count()
        total_clientes = Customers.objects.filter(is_active=True).count()

        utilidad = total_ventas - total_compras

        # Respuesta
        data = {
            "ventas": ventas_mes.count(),
            "total_ventas": total_ventas,
            "compras": compras_mes.count(),
            "total_compras": total_compras,
            "utilidad": utilidad,
            "clientes_nuevos": clientes_nuevos,
            "todos_los_clientes": total_clientes,
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
