from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View , generic
from .models import Cart , CartItem 
from django.shortcuts import get_object_or_404 , redirect
from products.models import Product


# Create your views here.

class AddToCartView(LoginRequiredMixin,View):
    def post(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        cart = Cart.objects.get(user=request.user)
        cartitem , created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        if not created:
            if cartitem.quantity < product.stock:
                cartitem.quantity += 1
                cartitem.save()
                return redirect ("cart:my_cart")
        else:
            cartitem.quantity = 1
            cartitem.save()
            return redirect ("cart:my_cart")        
        
class MyCartView(LoginRequiredMixin,generic.DetailView):
    template_name = "my_cart.html"
    context_object_name = "cart"

    def get_object(self, queryset = None):
        return Cart.objects.get(user=self.request.user)

class IncreaseQuantityView(LoginRequiredMixin,View):
    def post(self,request,pk):
        item = get_object_or_404(CartItem,pk=pk)
        if item.quantity < item.product.stock:
            item.quantity += 1
            item.save()
        return redirect ("cart:my_cart")
    
class DecreaseQuantityView(LoginRequiredMixin,View):
    def post(self,request,pk):
        item = get_object_or_404(CartItem,pk=pk)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            return redirect ("cart:my_cart")
        else:
            item.delete()
            return redirect ("cart:my_cart")
        
class DeleteFromCartView(LoginRequiredMixin,View):
    def post(self,request,pk):
        item = get_object_or_404(CartItem,pk=pk)
        item.delete()
        return redirect ("cart:my_cart")