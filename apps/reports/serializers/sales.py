# Django REST Framework
from rest_framework import serializers

from apps.reports.constant import ReportResponseFormatChoices, SalesReportTypeChoices


class SalesReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    type_report = serializers.ChoiceField(
        choices=SalesReportTypeChoices.choices
    )
    response_format =  serializers.ChoiceField(
        choices=ReportResponseFormatChoices.choices,
        required=False
    )