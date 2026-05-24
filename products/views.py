from django.views import generic
from .models import Slider , Product
from django.core.paginator import Paginator

class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(category__is_active=True,brand__is_active=True,is_published=True)
        context["sliders"] = Slider.objects.select_related("product").filter(product__is_active=True,product__is_published=True)[:3]
        context["promotionals"] = products.filter(is_promotional=True)[:5]
        trending_list = products.filter(is_trending=True)
        paginator = Paginator(trending_list,6)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)
        return context
    
class ProductListView(generic.ListView):
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(is_published=True).annotate()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = Product.objects.filter(is_published=True).count()
        return context