from django.http import HttpResponsePermanentRedirect


class WWWRedirectMiddleware(object):

    def process_request(self, request):
        if request.META['HTTP_HOST'].startswith('3cosystem.'):
            return HttpResponsePermanentRedirect('http://www.3cosystem.com')
