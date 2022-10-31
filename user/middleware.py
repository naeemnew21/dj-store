from project.settings import THEME_STYLE


class SetThemeSessionKeyMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        theme = request.COOKIES.get(THEME_STYLE, None)

        if theme:
            response = self.get_response(request)
        else:
            response = self.get_response(request)
            response.set_cookie(THEME_STYLE, 'light')

        return response