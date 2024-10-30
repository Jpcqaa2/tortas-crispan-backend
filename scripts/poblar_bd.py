from django.core.management import call_command


def poblar_datos_bd():
    call_command('loaddata', 'fixtures/departments.json')
    call_command('loaddata', 'fixtures/cities.json')
    call_command('loaddata', 'fixtures/groups.json')
    call_command('loaddata', 'fixtures/categories.json')
    call_command('loaddata', 'fixtures/customers.json')
    call_command('loaddata', 'fixtures/products.json')
    call_command('loaddata', 'fixtures/sales_status.json')
    call_command('loaddata', 'fixtures/sales.json')
    call_command('loaddata', 'fixtures/sales_details.json')
    call_command('loaddata', 'fixtures/article_types.json')
    call_command('loaddata', 'fixtures/articles.json')
    call_command('loaddata', 'fixtures/suppliers.json')

def run():
    print(">>> Inició creacion de datos en la BD...")
    poblar_datos_bd()
    print(">>> Finalizó creación de datos en la BD.")