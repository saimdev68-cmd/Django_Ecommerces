from products.models import Category , Brand , Product
from django.db.models import Prefetch

def all_things(request):
    products = Product.objects.filter(is_published=True)
    return {
        "brands":Brand.objects.filter(is_active=True)[:6],
        "categories":Category.objects.filter(is_active=True)[:7].prefetch_related(
            "brands",
            Prefetch(
                "products",
                queryset=products
            )
        )
    }