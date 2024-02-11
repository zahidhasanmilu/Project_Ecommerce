
from django.contrib.auth.models import AnonymousUser
from App_order.models import Cart,Order
from App_shop.models import Category


def categories(request):
    cate = Category.objects.filter(parent=None)
    context = {'cate': cate}
    return context


# Cart Count
def cart_count(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(
            user=request.user, purchased=False)
        order_queryset = Order.objects.filter(user=request.user, ordered=False)
        order = order_queryset.first()  # Fetch the first order if it exists
        cart_count = cart_item.count()
    else:
        cart_count = 0
        cart_item = 0
        order = 0

    context = {'cart_count': cart_count, 'cart_item': cart_item, 'order': order}
    return context