from django.http import HttpResponse
from django.views import View
import urllib.request

class GandhiAPIView(View):
    def get(self, request):
        url = 'http://busqueda.gandhi.com.mx/busca'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += '?q=' + request.GET.get('q')
        url.encode('utf-8')
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("Gandhi didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())
