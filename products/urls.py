from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("Products/",views.ProductListView.as_view(),name="products_list")
]