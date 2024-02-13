from apps.carts.models import Cart
from apps.products.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE = 'Product successfully added to your cart.'


@login_required
def add_product_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        user_carts = Cart.objects.filter(user=request.user, product=product).select_related('user', 'product')
        if user_carts.exists():
            cart = user_carts.first()
            cart.quantity += 1
            cart.save(update_fields=('quantity', 'updated_at'))
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

        return JsonResponse(
            data={
                'success': True,
                'notification': _(SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE),
            }
        )
    return redirect('products:my_products')
