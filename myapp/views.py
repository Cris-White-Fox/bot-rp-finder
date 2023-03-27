from django.http import HttpResponse
import datetime
from decouple import config


aaaa = 1
uptime = datetime.datetime.now()


# Create your views here.
def current_datetime(request):
    SECRET_KEY = config("TEST_KEY", default="123")
    now = datetime.datetime.now()
    global aaaa
    aaaa += 1
    html = f"<html><body>It is now {now}. test key = {SECRET_KEY}, aaaa = {aaaa}, uptime = {now - uptime}</body></html>"
    return HttpResponse(html)