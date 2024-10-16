# Generated by Django 4.2.11 on 2024-10-16 06:07

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
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=150)),
                ('presentation', models.CharField(max_length=100, null=True)),
                ('reference', models.CharField(max_length=100, null=True)),
                ('is_disposible', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'db_table': 'articles',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ArticleTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'article types',
                'verbose_name_plural': 'article types',
                'db_table': 'article_types',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('payment_method', models.CharField(choices=[('1', 'EFECTIVO'), ('2', 'NEQUI'), ('3', 'BANCOLOMBIA')], default='1', max_length=1)),
                ('description', models.CharField(max_length=150, null=True)),
                ('purchase_date', models.DateField()),
                ('total', models.BigIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'purchases',
                'verbose_name_plural': 'purchases',
                'db_table': 'purchases',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.CharField(max_length=150)),
                ('cell_phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('establishment_address', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.city')),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
                'db_table': 'suppliers',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PurchasesDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.BigIntegerField(default=0)),
                ('measurment_unit', models.CharField(choices=[('1', 'Gramos'), ('2', 'Kilo Gramo'), ('3', 'Libra'), ('4', 'Litro')], max_length=1)),
                ('subtotal', models.BigIntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.articles')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.purchases')),
            ],
            options={
                'verbose_name': 'purchases details',
                'verbose_name_plural': 'purchases details',
                'db_table': 'purchases_details',
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='purchases',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.suppliers'),
        ),
        migrations.AddField(
            model_name='purchases',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articles',
            name='article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.articletypes'),
        ),
    ]