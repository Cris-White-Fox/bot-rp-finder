from django.http import HttpResponse
import datetime
from decouple import config


# Create your views here.
def current_datetime(request):
    SECRET_KEY = config("TEST_KEY", default="123")
    now = datetime.datetime.now()
    html = f"<html><body>It is now {now}. test key = {SECRET_KEY} </body></html>"
    return HttpResponse(html)