from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from services.basket.basket import Basket
from services.basket.basket import BasketManager


@login_required
def show_basket(request):
    context = {'title': 'Basket'}

    return render(request, 'basket/index.html', context=context)


@login_required
def add_basket(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).add_product()

    return redirect('products:detail_product', product_id)


@login_required
def add_product(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).add_product()

    return redirect('baskets:show')


@login_required
def sub_product(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).sub_product()

    return redirect('baskets:show')


@login_required
def change_basket(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).change_basket_quantity()

    return redirect('baskets:show')


@login_required
def remove_basket(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).remove_basket()

    return redirect('baskets:show')


@login_required
def clear_basket(request):
    basket = Basket(request)
    BasketManager(basket).clear_basket()

    return redirect('baskets:show')
