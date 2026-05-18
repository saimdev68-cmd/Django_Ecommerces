from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order , OrderItem
from django.shortcuts import get_object_or_404 , redirect , render
from django.views import View , generic
from cart.models import Cart
from django.db import transaction
import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib import messages

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderListView(LoginRequiredMixin,generic.ListView):
    template_name = "order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-id")

class OrderInformationView(LoginRequiredMixin,View):
    template_name = "order_information.html"
    def get(self,request):
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        if not items:
            return redirect ("cart:my_cart")
        data = request.session.get("order_information",{})
        return render (request,self.template_name,{"data":data})
    def post(self,request):
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        if not items:
            return redirect ("cart:my_cart")
        request.session["order_information"] = {
            "full_name":request.POST.get("full_name"),
            "phone_number":request.POST.get("phone_number"),
            "address":request.POST.get("address")
        }
        return redirect ("order:checkout")

class CheckoutView(LoginRequiredMixin,View):
    def get(self,request):
        data = request.session.get("order_information",{})
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        if not data:
            return redirect ("order:order_information")
        return render (request,"checkout.html",{
            "data":data,
            "items":items,
            "cart":cart
        })
    def post(self,request):
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        line_lines = []
        for item in items:
            line_lines.append({
                "price_data":{
                    "currency":"usd",
                    "product_data":{
                        "name":item.product.name,
                    },
                    "unit_amount":int(item.total_price * 100)
                },
                "quantity":item.quantity
            })
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_lines,
            mode="payment",
            success_url=request.build_absolute_uri(reverse("order:success"))+"?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("order:checkout"))
        )
        return redirect (session.url)

class PaymentSuccessView(LoginRequiredMixin,View):
    def get(self,request):
        session_id = request.GET.get("session_id")
        data = request.session.get("order_information")
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()

        if not session_id:
            return redirect ("store:my_cart")
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception as e:
            messages.error(request,"Payment verification is failed.")
            return redirect ("store:home")
        
        if session.payment_status != "paid":
            messages.error(request,"Payment not completed")
            return redirect ("store:home")
        
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=data.get("full_name"),
                phone_number=data.get("phone_number"),
                address=data.get("address"),
                grand_total=cart.grand_total,
                stripe_session_id=session_id,
                is_paid=True
            )
            for item in items:
                product = item.product
                product.stock -= item.quantity
                product.save()
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price,
                )
            del request.session['order_information']
            items.delete()
        messages.success(request,"Payment Successfully , Order placed.")
        return redirect ("store:home")