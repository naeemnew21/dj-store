from project.settings import CART_SESSION_ID_KEY
import uuid


class SetCartSessionKeyMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        cart_key = request.COOKIES.get(CART_SESSION_ID_KEY, None)

        if cart_key:
            response = self.get_response(request)
        else:
            cart_id = str(uuid.uuid4())
            response = self.get_response(request)
            response.set_cookie(CART_SESSION_ID_KEY, cart_id)

        return response