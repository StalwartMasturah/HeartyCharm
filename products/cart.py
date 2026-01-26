# cart.py
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add or update product quantity in the cart.
        If override_quantity=True, set quantity exactly.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            if override_quantity:
                # Set quantity but check stock
                self.cart[product_id]['quantity'] = min(quantity, product.stock)
            else:
                # Increase quantity but do not exceed stock
                new_qty = self.cart[product_id]['quantity'] + quantity
                self.cart[product_id]['quantity'] = min(new_qty, product.stock)
        else:
            self.cart[product_id] = {'quantity': min(quantity, product.stock), 'price': str(product.price)}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        from products.models import Product
        items = []
        for product_id, details in self.cart.items():
            product = Product.objects.get(id=product_id)
            item = {
                'product': product,
                'quantity': details['quantity'],
                'total_price': product.price * details['quantity']
            }
            items.append(item)
        return items

    def get_total_price(self):
        return sum(item['total_price'] for item in self.get_items())
