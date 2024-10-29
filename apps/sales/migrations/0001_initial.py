# Generated by Django 4.2.11 on 2024-10-28 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'categories',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=150)),
                ('identification_type', models.CharField(choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería')], max_length=2)),
                ('identification_number', models.CharField(max_length=20)),
                ('cell_phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('residential_address', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.city')),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
                'db_table': 'customers',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=150)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('measurement_unit', models.CharField(choices=[('g', 'Gramo'), ('kg', 'Kilogramo'), ('l', 'Litro'), ('unit', 'Unidad')], default='unit', max_length=4)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.URLField(blank=True, max_length=255, null=True)),
                ('featured_product', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.categories')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'products',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('payment_method', models.CharField(choices=[('1', 'Efectivo'), ('2', 'Tarjeta de Crédito'), ('3', 'Nequi')], default='1', max_length=1)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='sales.customers')),
            ],
            options={
                'verbose_name': 'sale',
                'verbose_name_plural': 'sales',
                'db_table': 'sales',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SalesStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'sales status',
                'verbose_name_plural': 'sales statuses',
                'db_table': 'sales_status',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'test_model',
            },
        ),
        migrations.CreateModel(
            name='SalesDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('quantity', models.IntegerField(default=1)),
                ('unit_value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_details', to='sales.products')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_details', to='sales.sales')),
            ],
            options={
                'verbose_name': 'sale detail',
                'verbose_name_plural': 'sales details',
                'db_table': 'sales_details',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='sales',
            name='sale_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.salesstatus'),
        ),
        migrations.AddField(
            model_name='sales',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to=settings.AUTH_USER_MODEL),
        ),
    ]
