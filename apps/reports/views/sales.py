# Django
from django.http import HttpResponse
from django.http import JsonResponse

# Django Rest Framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ValidationError

# Django models
from django.db.models import F

# Utils
import io
import pandas as pd
from django_pandas.io import read_frame

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Models
from apps.reports.constant import ReportResponseFormatChoices
from apps.reports.filters import SalesReportFilter
from apps.reports.serializers.sales import SalesReportSerializer
from apps.sales.models.sales import Sales
from apps.utils.logic.reports import df_to_excel, format_currency
from apps.utils.serializers.globals import WithChoicesSerializer


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
        
        queryset = Sales.objects\
            .filter(is_active=True)\
            .annotate(
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
