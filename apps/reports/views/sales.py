# Django
from django.http import HttpResponse, JsonResponse
from django.db.models import F, Sum, Count
from django.utils.timezone import now
from datetime import datetime

# Django Rest Framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ValidationError

# Utils
from django_pandas.io import read_frame
from apps.utils.logic.reports import df_to_excel, format_currency

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Models
from apps.sales.models.sales import Sales
from apps.purchases.models.purchases import Purchases
from apps.sales.models.customers import Customers

# Filters y Serializers
from apps.reports.filters import SalesReportFilter
from apps.reports.serializers.sales import SalesReportSerializer
from apps.utils.serializers.globals import WithChoicesSerializer
from apps.reports.constant import ReportResponseFormatChoices


class SalesReportsViewset(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=SalesReportSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_FILE,
                description='reporte_general_de_ventas.xlsx'
            ),
        }
    )
    @action(detail=False, methods=["GET"])
    def general(self, request, *args, **kwargs):
        serializer = SalesReportSerializer(
            data=request.GET,
        )
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        queryset = Sales.objects.filter(is_active=True).annotate(
            fecha=F('sale_date'),
            metodo_pago=WithChoicesSerializer(Sales, 'payment_method'),
            estado=F('sale_status__name'),
            cliente=F('customer__name'),
            categoria=F('salesdetails__product__category__name'),
            producto=F('salesdetails__product__name'),
            cantidad=F('salesdetails__quantity'),
            precio_unitario=F('salesdetails__unit_value'),
            subtotal=F('salesdetails__subtotal'),
            total_venta=F('total'),
        )

        report_filter = SalesReportFilter(serializer_data, queryset=queryset)
        queryset = report_filter.qs.order_by('id')

        if not queryset.exists():
            raise ValidationError({'detail': ['No existen datos para las fechas dadas.']})

        reporte = read_frame(queryset)

        # Formato moneda
        reporte['precio_unitario'] = reporte['precio_unitario'].apply(format_currency)
        reporte['subtotal'] = reporte['subtotal'].apply(format_currency)
        reporte['total_venta'] = reporte['total_venta'].apply(format_currency)

        # Establecer todas las filas de 'total_venta' a NaN excepto la primera fila de cada venta (mismo 'id')
        reporte['total_venta'] = reporte['total_venta'].mask(reporte.duplicated(subset=['id']))

        order_columns = ['id', 'cliente', 'fecha', 'estado', 'metodo_pago', 'categoria',
                         'producto', 'cantidad', 'precio_unitario', 'subtotal', 'total_venta']
        reporte = reporte[order_columns]

        if serializer_data.get('response_format') == ReportResponseFormatChoices.EXCEL:
            workbook = df_to_excel(reporte, sheet_name="reporte_general_de_ventas")
            response = HttpResponse(workbook, content_type="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=reporte_general_de_ventas.xlsx'
            return response

        reporte = reporte.fillna('')
        json_data = reporte.to_dict(orient='records')
        return JsonResponse(json_data, safe=False)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'fecha_actual',
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
                    'clientes_nuevos_del_mes': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'todos_los_clientes': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        }
    )
    @action(detail=False, methods=["GET"])
    def dashboard_metrics(self, request, *args, **kwargs):
        # Obtener parámetro de fecha actual
        fecha_actual = request.query_params.get("fecha_actual")
        if fecha_actual:
            try:
                fecha = datetime.strptime(fecha_actual, "%Y-%m-%d")
            except ValueError:
                raise ValidationError({'detail': ["Formato de fecha inválido. Use YYYY-MM-DD"]})
        else:
            fecha = now()

        mes_actual = fecha.month
        año_actual = fecha.year

        # Cálculos
        ventas_mes = Sales.objects.filter(created__year=año_actual, created__month=mes_actual, is_active=True)
        total_ventas = ventas_mes.aggregate(total=Sum("total"))["total"] or 0

        compras_mes = Purchases.objects.filter(purchase_date__year=año_actual, purchase_date__month=mes_actual, is_active=True)
        total_compras = compras_mes.aggregate(total=Sum("total"))["total"] or 0

        clientes_nuevos = Customers.objects.filter(created__year=año_actual, created__month=mes_actual).count()
        total_clientes = Customers.objects.count()

        utilidad = total_ventas - total_compras

        # Respuesta
        data = {
            "ventas": ventas_mes.count(),
            "total_ventas": total_ventas,
            "compras": compras_mes.count(),
            "total_compras": total_compras,
            "utilidad": utilidad,
            "clientes_nuevos_del_mes": clientes_nuevos,
            "todos_los_clientes": total_clientes,
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
