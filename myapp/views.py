from django.shortcuts import render
import requests
from requests.exceptions import MissingSchema, InvalidURL, ConnectionError
from django.http import HttpResponseRedirect
from django.contrib import messages
from bs4 import BeautifulSoup

from .models import Link


# Create your views here.
def scrape(request):
    if request.method == 'POST':
        try:
            site = 'http://' + request.POST.get('site', '')

            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string
                Link.objects.create(address=link_address, name=link_text)
        except (MissingSchema, ConnectionError, InvalidURL):
            messages.add_message(request, messages.ERROR, 'The link you provided was not found. Please try again.')

        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()

    return render(request, 'myapp/result.html', {'data': data})


def clear(request):
    Link.objects.all().delete()
    return render(request, 'myapp/result.html')
