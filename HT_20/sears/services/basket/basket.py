from django.contrib import messages


class Basket:
    def __init__(self, request, product_id=None):
        self.request = request
        self.product_id = product_id
        self.product = self._get_product()
        self.name = self._get_product_name()
        self.quantity = self._get_quantity()
        self.price = self._get_price()

    def _get_product(self):
        return self.request.session.setdefault('baskets', {}).get(self.product_id, {})

    def _get_product_name(self):
        name = self.request.POST.get('name')
        if name:
            return name
        return self.product.get('name', '')

    def _get_quantity(self):
        return int(self.product.get('quantity', 0))

    def _get_price(self):
        try:
            price = round(float(self.request.POST.get('price')), 2)
        except TypeError:
            price = self.product.get('price', 0)

        return price

    def _get_product_total_price(self):
        return round(float(self.price * self.quantity), 2)

    def _update_product(self):
        self.product.update({
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'total_price': self._get_product_total_price(),
        })

    def update_basket(self):
        self._update_product()
        self.request.session['baskets'].update({self.product_id: self.product})
        self.request.session['total_price'] = self.get_basket_total_price()
        self.request.session.modified = True

    def get_basket_total_price(self):
        baskets = self.request.session.get('baskets', {})
        return round(sum(float(product.get('total_price', 0)) for product in baskets.values()), 2)


class BasketManager:
    ERROR_MESSAGE = 'The quantity must be between 1 and 100.'
    UPDATE_MESSAGE = 'Product {} has been updated.'

    def __init__(self, basket):
        self.basket = basket

    def add_product(self):
        if self.basket.quantity == 0:
            self.basket.quantity += 1
            messages.success(self.basket.request, 'Product added to basket.')
        elif 0 < (self.basket.quantity + 1) < 101:
            self.basket.quantity += 1
            messages.success(self.basket.request, self.UPDATE_MESSAGE.format(self.basket.product_id))
        else:
            messages.error(self.basket.request, self.ERROR_MESSAGE)

        self.basket.update_basket()
        return self

    def sub_product(self):
        if 0 < (self.basket.quantity - 1) < 101:
            self.basket.quantity -= 1
            messages.success(self.basket.request, self.UPDATE_MESSAGE.format(self.basket.product_id))
        else:
            messages.error(self.basket.request, self.ERROR_MESSAGE)

        self.basket.update_basket()
        return self

    def change_basket_quantity(self):
        quantity = int(self.basket.request.POST.get('quantity', 0))
        if 0 < quantity < 101:
            self.basket.quantity = quantity
            self.basket.update_basket()
            messages.success(self.basket.request, self.UPDATE_MESSAGE.format(self.basket.product_id))
        else:
            messages.error(self.basket.request, self.ERROR_MESSAGE)
        return self

    def remove_basket(self):
        baskets = self.basket.request.session.get('baskets', {})
        if self.basket.product_id in baskets:
            del baskets[self.basket.product_id]
            self.basket.request.session['baskets'] = baskets
            self.basket.request.session['total_price'] = self.basket.get_basket_total_price()
            self.basket.request.session.modified = True
            messages.success(self.basket.request, f'Deleted {self.basket.product_id} from basket.')

    def clear_basket(self):
        if self.basket.request.session.get('baskets'):
            del self.basket.request.session['baskets']
            del self.basket.request.session['total_price']
            self.basket.request.session.modified = True
            messages.success(self.basket.request, 'Basket cleared!')
