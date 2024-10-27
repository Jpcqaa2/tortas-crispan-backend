from django.db import models

class Sales(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_id = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('payments.PaymentMethod', on_delete=models.CASCADE)
    sale_status = models.ForeignKey('statuses.SaleStatus', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sales'

    def __str__(self):
        return f'Sale {self.id} - Total: {self.total}'
