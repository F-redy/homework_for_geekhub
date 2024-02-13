from django.shortcuts import redirect
from django.shortcuts import render
from services.basket.basket import Basket
from services.basket.basket import BasketManager


def show_basket(request):
    context = {'title': 'Basket'}

    return render(request, 'basket/index.html', context=context)


def add_basket(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).add_product()

    return redirect('products:detail_product', product_id)


def add_product(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).add_product()

    return redirect('baskets:show')


def sub_product(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).sub_product()

    return redirect('baskets:show')


def change_basket(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).change_basket_quantity()

    return redirect('baskets:show')


def remove_basket(request, product_id):
    basket = Basket(request, product_id)
    BasketManager(basket).remove_basket()

    return redirect('baskets:show')


def clear_basket(request):
    basket = Basket(request)
    BasketManager(basket).clear_basket()

    return redirect('baskets:show')
