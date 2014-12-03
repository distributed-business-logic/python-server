from json import dumps, load, loads
from platform import node
from socket import gethostbyname, gethostname
from urllib2 import urlopen
from urlparse import urljoin

from klein import Klein

from __init__ import __version__

base_url = '/api'
class PackageServer(object):
    app = Klein()
    number = 0
    packages = {}  # Use a db with a cache instead during production

    @app.route('/')
    def root(self, request):
        request.setHeader('Content-Type', 'application/json')
        request.setResponseCode(501)

        return dumps(dict(error='Not implemented or not found',
                          error_message="Route '{url}' wasn't found".format(url=request.URLPath().path)))

    @app.route(urljoin(base_url, '/'))
    @app.route(urljoin(base_url, '/status'))
    def status(self, request):
        request.setHeader('Content-Type', 'application/json')
        print type(request)
        print request.__class__

        self.number += 1
        return dumps({
            'request_number': self.number,
            'ip': {
                'private': gethostbyname(gethostname()),
                'public': load(urlopen('http://httpbin.org/ip'))['origin']
            }, 'version': __version__, 'host': node()
        })

    @app.route(urljoin(base_url, '/upload'), methods=['POST'])
    def upload_package(self, request):
        request.setHeader('Content-Type', 'application/json')
        print type(request)
        return dumps(request.args or loads(request.content.read()))

    @app.route(urljoin(base_url, '/:package_name'), methods=['GET'])
    def retrieve_package(self, request):
        request.setHeader('Content-Type', 'application/json')
        print type(request)
        return dumps(self.packages.get(request.params.package_name))


if __name__ == '__main__':
    PackageServer().app.run('0.0.0.0', 8080)
