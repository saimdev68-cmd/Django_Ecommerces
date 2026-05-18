from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("list/",views.OrderListView.as_view(),name="order_list"),
    path("information/",views.OrderInformationView.as_view(),name="order_information"),
    path("checkout/",views.CheckoutView.as_view(),name="checkout"),
    path("success/",views.PaymentSuccessView.as_view(),name="success")
]
