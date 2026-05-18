from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("<int:pk>/add_to_cart/",views.AddToCartView.as_view(),name="add_to_cart"),
    path("my_cart/",views.MyCartView.as_view(),name="my_cart"),
    path('<int:pk>/increase_quantity/',views.IncreaseQuantityView.as_view(),name="increase_quantity"),
    path('<int:pk>/decrease_quantity/',views.DecreaseQuantityView.as_view(),name="decrease_quantity"),
    path('<int:pk>/delete_from_cart/',views.DeleteFromCartView.as_view(),name="delete_from_cart"),
]
