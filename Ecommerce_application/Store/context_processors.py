from .models import Cart
from .models import userData
def cart_counter(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = userData.objects.get(id=user_id)
            cart_count = Cart.objects.filter(user=user).count()
        except userData.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return {'cart_count': cart_count}
