from .models import Product

def get_categories(request):
    categories=set()
    products=Product.objects.values_list('category')
    categories=set(products)
    p=[x[0] for x in categories]
    return {
        'categories':[x[0] for x in categories]
    }
