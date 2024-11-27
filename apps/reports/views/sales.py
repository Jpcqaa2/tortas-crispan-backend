# Django
from django.http import HttpResponse

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
from apps.reports.filters import SalesReportFilter
from apps.reports.serializers.sales import SalesReportSerializer
from apps.sales.models.sales import Sales
from apps.utils.logic.reports import size_column_excel
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
                fecha=F('created__date'), 
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

        sio = io.BytesIO()
        reporte = read_frame(queryset)

        # Establecer todas las filas de 'total_venta' a NaN excepto la primera fila de cada venta (mismo 'id')
        reporte['total_venta'] = reporte['total_venta'].mask(reporte.duplicated(subset=['id']))

        order_columns = ['id', 'cliente', 'fecha', 'estado', 'metodo_pago', 'categoria', 
                         'producto', 'cantidad', 'precio_unitario', 'subtotal', 'total_venta']
        reporte = reporte[order_columns]

        excel = pd.ExcelWriter(sio, engine='xlsxwriter')
        reporte.to_excel(excel, sheet_name="reporte_general_de_ventas", index=False)
        size_column_excel(excel, reporte, 'reporte_general_de_ventas')

        excel.close()
        sio.seek(0)
        workbook = sio.getvalue()

        response = HttpResponse(workbook, content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=reporte_general_de_ventas.xlsx'
        return response
