# Django
from django.http import HttpResponse, JsonResponse
from django.db.models import F

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
from apps.purchases.models.purchases import Purchases

# Filters y Serializers
from apps.reports.filters import PurchaseReportFilter
from apps.reports.serializers.purchases import PurchaseReportSerializer
from apps.utils.serializers.globals import WithChoicesSerializer
from apps.reports.constant import ReportResponseFormatChoices


class PurchaseReportsViewset(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=PurchaseReportSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_FILE,
                description='reporte_general_de_compras.xlsx'
            ),
        }
    )
    @action(detail=False, methods=["GET"])
    def general(self, request, *args, **kwargs):
        serializer = PurchaseReportSerializer(
            data=request.GET,
        )
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        queryset = Purchases.objects.filter(is_active=True).annotate(
            fecha=F('purchase_date'),
            metodo_pago=WithChoicesSerializer(Purchases, 'payment_method'),
            proveedor=F('supplier__name'),
            tipo_articulo=F('purchasesdetails__article__article_type__name'),
            articulo=F('purchasesdetails__article__name'),
            cantidad=F('purchasesdetails__quantity'),
            precio_unitario=F('purchasesdetails__unit_price'),
            subtotal=F('purchasesdetails__subtotal'),
            total_compra=F('total'),
            descripcion=F('description'),
            unidad_medida=F('purchasesdetails__measurment_unit'),
        )

        report_filter = PurchaseReportFilter(serializer_data, queryset=queryset)
        queryset = report_filter.qs.order_by('id')

        if not queryset.exists():
            raise ValidationError({'detail': ['No existen datos para las fechas dadas.']})

        reporte = read_frame(queryset)

        # Formato moneda
        reporte['precio_unitario'] = reporte['precio_unitario'].apply(format_currency)
        reporte['subtotal'] = reporte['subtotal'].apply(format_currency)
        reporte['total_compra'] = reporte['total_compra'].apply(format_currency)

        # Establecer todas las filas de 'total_compra' a NaN excepto la primera fila de cada venta (mismo 'id')
        reporte['total_compra'] = reporte['total_compra'].mask(reporte.duplicated(subset=['id']))

        order_columns = ['id', 'proveedor', 'fecha', 'descripcion', 'metodo_pago', 'tipo_articulo',
                         'articulo', 'cantidad', 'unidad_medida', 'precio_unitario', 'subtotal', 'total_compra']
        reporte = reporte[order_columns]

        if serializer_data.get('response_format') == ReportResponseFormatChoices.EXCEL:
            workbook = df_to_excel(reporte, sheet_name="reporte_general_de_compras")
            response = HttpResponse(workbook, content_type="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=reporte_general_de_compras.xlsx'
            return response

        reporte = reporte.fillna('')
        json_data = reporte.to_dict(orient='records')
        return JsonResponse(json_data, safe=False)
