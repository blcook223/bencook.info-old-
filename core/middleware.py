"""
Middleware for core app.
"""

from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import resolve
from django.core import urlresolvers
from django.utils.http import urlquote


# http://eikke.com/django-domain-redirect-middleware/
class DomainRedirectMiddleware(object):
    """
    Redirect to canonical domains.
    """

    def process_request(self, request):
        """
        Return permanent redirect to correct domain.
        """
        host = request.get_host()
        site = Site.objects.get_current()

        if host == site.domain:
            return None

        try:
            resolve(request.path)
        except urlresolvers.Resolver404:
            return None

        new_uri = '%s://%s%s%s' % (
                request.is_secure() and 'https' or 'http',
                site.domain,
                urlquote(request.path),
                (request.method == 'GET' and len(request.GET) > 0) and
                    '?{0}'.format(request.GET.urlencode()) or
                    ''
            )

        return HttpResponsePermanentRedirect(new_uri)
