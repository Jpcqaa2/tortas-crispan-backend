from .sales import Sales
from .sales_details import SalesDetails
from .categories import Categories
from .customers import Customers
from .products import Products
from .sales_status import SalesStatus


# Lista de modelos exportados para facilitar importaciones en otras partes del proyecto
__all__ = [
    "Categories",
    "Customers",
    "Products",
    "Sales",
    "SalesDetails",
    "SalesStatus",
]
