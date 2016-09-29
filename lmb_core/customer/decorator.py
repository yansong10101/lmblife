from rest_framework import status
from django.http.response import HttpResponse


def customer_login_required(func):
    def wrapped(request, *args, **kwargs):
        customer = request.COOKIES.get('customer')
        if not customer:
            return HttpResponse(content='Unauthorized ! Login Required !', status=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)
    return wrapped
