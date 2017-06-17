from django.http import HttpResponse
from django.views import View
import urllib.request

class GandhiAPIView(View):
    def get(self, request):
        url = 'http://busqueda.gandhi.com.mx/busca'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += '?q=' + request.GET.get('q')
        url += '&common_filter%5B400%5D=448%7C568' # only books filter
        url.encode('utf-8')
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("Gandhi didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())

class ElSotanoAPIView(View):
    def get(self, request):
        url = 'https://www.elsotano.com/busqueda.php'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += '?q=' + request.GET.get('q')
        url += '&c=1' # only books filter
        url.encode('utf-8')
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("El Sotano didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())

class ElPenduloAPIView(View):
    def get(self, request):
        url = 'https://pendulo.com/buscar/'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += '?idFormato=6' # only books filter
        url += '&search_string=' + request.GET.get('q')
        url.encode('utf-8')
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("El Pendulo didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())
