from django import template

register = template.Library()



def get_list(d):
    try:
        stars = [0 for i in range(5)]
        for i in range(int(d)):
            stars[i] = 1
        if d-int(d) > 0:
            stars[int(d)] = 0.5
        value = stars
    except:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value


get_list = register.filter('get_list', get_list)