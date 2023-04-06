from django.shortcuts import render
import requests
from requests.exceptions import MissingSchema, InvalidURL, ConnectionError
from django.http import HttpResponseRedirect
from django.contrib import messages
from bs4 import BeautifulSoup

from .models import Link


def scrape(request):
    """
    Django view.
    Display main page with website form and list of links from database.
    If request method is POST, scrape the given website and add found links to database.

    :param request: Django request
    :return: rendered result.html template
    """
    if request.method == 'POST':
        try:
            site = 'http://' + request.POST.get('site', '')

            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            # find all anchor tags
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
    """
    Django view.
    Delete all Link objects in the database.

    :param request: Django request
    :return: rendered result.html template
    """

    Link.objects.all().delete()
    return render(request, 'myapp/result.html')
