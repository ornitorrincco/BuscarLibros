from django.http import HttpResponse
from django.views import View
import urllib.request
import re
import gzip

class GandhiAPIView(View):
    def get(self, request):
        url = 'http://busqueda.gandhi.com.mx/busca'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += '?q=' + request.GET.get('q')
        url += '&common_filter%5B400%5D=448%7C568' # only books filter
        url = re.sub(r"\s+", '+', url)
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
        url = re.sub(r"\s+", '+', url)
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
        url = re.sub(r"\s+", '+', url)
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("El Pendulo didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())

class PorruaAPIView(View):
    def get(self, request):
        url = 'https://www.porrua.mx/busqueda/todos/'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += request.GET.get('q') + '/todos/1/impreso'
        url.encode('utf-8')
        url = re.sub(r"\s+", '+', url)
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("Porrua didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())

class EducalAPIView(View):
    def get(self, request):
        url = 'http://www.educal.com.mx/busca/fisico/'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        url += request.GET.get('q') + '/pagina1.html'
        url.encode('utf-8')
        url = re.sub(r"\s+", '_', url)
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return HttpResponse("Educal didn't ansered 200 OK").status_code(400) # bad request
        return HttpResponse(response.read())

class FCEAPIView(View):
    def get(self, request):
        url = 'https://www.fondodeculturaeconomica.com/ResultadoE.aspx'
        if len(request.GET) == 0 or 'q' not in request.GET:
            return HttpResponse('queryParams missing or wrong').status_code(400) # bad request
        headers = {
            'Host':'www.fondodeculturaeconomica.com',
            'Connection':'keep-alive',
            'Content-Length':'3536',
            'Origin':'https://www.fondodeculturaeconomica.com',
            'Cache-Control':'no-cache',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'X-MicrosoftAjax':'Delta=true',
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en',
            'Cookie':'ASP.NET_SessionId=vcf3ru445xrcg0oy41f5cxmt; Settings=CUENTA=0&IMPORTE=0&PEDIDO=158612253'
        }
        values = "ctl00%24ToolkitScriptManager1=ctl00%24contenido%24updateSearch%7Cctl00%24contenido%24triggerSearch&ToolkitScriptManager1_HiddenField=%3B%3BAjaxControlToolkit%2C%20Version%3D3.5.40412.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D28f01b0e84b6d53e%3Aes-ES%3A1547e793-5b7e-48fe-8490-03a375b13a33%3A475a4ef5%3A5546a2b%3Ad2e10b12%3Aeffe2a26%3A37e2e5c9%3A5a682656%3A12bbc599&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTcyMDc5NTQ0OQ9kFgJmD2QWAgIDD2QWAgIED2QWAgIJD2QWAmYPZBYGAgUPFCsAAg8WBB4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudAIMZGQWAmYPZBYYAgEPZBYCAgEPEA8WAh4EVGV4dAUpQU5UUk9QT0xPR8ONQSAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZGRkAgIPZBYCAgEPEA8WAh8CBShCUkVWSUFSSU9TICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGRkZAIDD2QWAgIBDxAPFgIfAgUpQlJFVklBUklPUyBERSBDSUVOQ0lBIENPTlRFTVBPUsOBTkVBICAgICBkZGRkAgQPZBYCAgEPEA8WAh8CBSlDSUVOQ0lBIFkgVEVDTk9MT0fDjUEgICAgICAgICAgICAgICAgICAgIGRkZGQCBQ9kFgICAQ8QDxYCHwIFKUNPTEVDQ0nDk04gUE9QVUxBUiAgICAgICAgICAgICAgICAgICAgICAgZGRkZAIGD2QWAgIBDxAPFgIfAgUoRElBTk9JQSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkZGQCBw9kFgICAQ8QDxYCHwIFKUVESUNJT05FUyBDSUVOVMONRklDQVMgVU5JVkVSU0lUQVJJQVMgICAgZGRkZAIID2QWAgIBDxAPFgIfAgUpRklMT1NPRsONQSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZGRkAgkPZBYCAgEPEA8WAh8CBShMQSBDSUVOQ0lBIFBBUkEgVE9ET1MgICAgICAgICAgICAgICAgICAgZGRkZAIKD2QWAgIBDxAPFgIfAgUoTElCUk9TIERFIFRFWFRPIERFIFNFQ1VOREFSSUEgICAgICAgICAgIGRkZGQCCw9kFgICAQ8QDxYCHwIFKFBBSURFSUEgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZGRkAgwPZBYCAgEPEA8WAh8CBShURVpPTlRMRSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGRkZAIHDxQrAAJkZGQCCQ8UKwACZBAWABYAFgBkGAQFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYOBRpjdGwwMCRjb250ZW5pZG8kY3VhZHJpY3VsYQUVY3RsMDAkY29udGVuaWRvJGxpc3RhBS9jdGwwMCRjb250ZW5pZG8kZmlsdHJvRWRpdG9yaWFsJGN0cmwwJGVkaXRvcmlhbAUvY3RsMDAkY29udGVuaWRvJGZpbHRyb0VkaXRvcmlhbCRjdHJsMSRlZGl0b3JpYWwFL2N0bDAwJGNvbnRlbmlkbyRmaWx0cm9FZGl0b3JpYWwkY3RybDIkZWRpdG9yaWFsBS9jdGwwMCRjb250ZW5pZG8kZmlsdHJvRWRpdG9yaWFsJGN0cmwzJGVkaXRvcmlhbAUvY3RsMDAkY29udGVuaWRvJGZpbHRyb0VkaXRvcmlhbCRjdHJsNCRlZGl0b3JpYWwFL2N0bDAwJGNvbnRlbmlkbyRmaWx0cm9FZGl0b3JpYWwkY3RybDUkZWRpdG9yaWFsBS9jdGwwMCRjb250ZW5pZG8kZmlsdHJvRWRpdG9yaWFsJGN0cmw2JGVkaXRvcmlhbAUvY3RsMDAkY29udGVuaWRvJGZpbHRyb0VkaXRvcmlhbCRjdHJsNyRlZGl0b3JpYWwFL2N0bDAwJGNvbnRlbmlkbyRmaWx0cm9FZGl0b3JpYWwkY3RybDgkZWRpdG9yaWFsBS9jdGwwMCRjb250ZW5pZG8kZmlsdHJvRWRpdG9yaWFsJGN0cmw5JGVkaXRvcmlhbAUwY3RsMDAkY29udGVuaWRvJGZpbHRyb0VkaXRvcmlhbCRjdHJsMTAkZWRpdG9yaWFsBTBjdGwwMCRjb250ZW5pZG8kZmlsdHJvRWRpdG9yaWFsJGN0cmwxMSRlZGl0b3JpYWwFGmN0bDAwJGNvbnRlbmlkbyREYXRhUGFnZXIxDzwrAAQBA2ZkBRxjdGwwMCRjb250ZW5pZG8kbHZSZXN1bHRhZG9zDzwrAA4CDGYNAgpkBR9jdGwwMCRjb250ZW5pZG8kZmlsdHJvRWRpdG9yaWFsDxQrAA5kZGRkZGRkPCsADAACDGRkZGYC%2F%2F%2F%2F%2Fw9k0sd6QiB35UkM13zk3Hi7DQa53mET0bCpa5RpayDk3zM%3D&__VIEWSTATEGENERATOR=8D69C3FB&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=0&__EVENTVALIDATION=%2FwEdABbFpnWIB8hRtK3R%2FssxR24Ur1LkQHwy8y8SvZsJjX1wWVNfKYw9bzVl1com8k%2BifejsWxOrp%2B4IqU3TtknTcBF%2FbH3KGOkBYCz0RdK%2B5koznXXyTjFfsnTilfBWCAYTqm%2FpL5V34ezGr0cxz7PF8rm0rGhk0LCgkb1DIRvup1ofpHsYUz%2F%2B%2BxWvWXfvJbQxJoSfnlxamIFLJKtKxEwmx3OTPdokrMtas%2Bu%2BIi0g9c7%2BxmWArShibfq9TOZa3TAx3YS0VwdPbX2j9IMOliIiCsVdZktg6zkQHLspAPDw9%2BOjbNpSTw1nNGBZp%2F%2Bu%2FB1wp%2F28CIZnWHhbVt68AMs3yqM5dxwYePubIlNWHlKOqQZAugO9acawarCiSRLo6an6POp4dtSp9NoTG%2BOW2xBESBHcU9K%2FePMErv%2Blb5ISRcISPZlRA9vHppox2H0gR1CrVmwCZ5a4FBg6E9VGoq%2BqBfIdjdIO7rMoLWMIvg%2B4rMBZG3N1n1a7S6tZOE%2Fe6lIMB6c%3D&ctl00%24contenido%24orderby=Relevancia&hiddenInputToUpdateATBuffer_CommonToolkitScripts=1&__ASYNCPOST=true&ctl00%24contenido%24triggerSearch=Search"
        data = values.encode("utf-8")
        url += '?buscar=' + request.GET.get('q')
        url.encode('utf-8')
        url = re.sub(r"\s+", '+', url)
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        if response.status != 200:
            return HttpResponse("FCE didn't ansered 200 OK").status_code(400) # bad request
        resp = gzip.decompress(response.read())
        return HttpResponse( str(resp,'utf-8') )
