""" Blackbox testing to enable same tests across multiple language-implementations of the protocol/services """

from unittest import TestCase, main as unittest_main
from urlparse import urljoin

import requests as http


class TestPackageServer(TestCase):
    uri = 'http://localhost:8080'

    @classmethod
    def setUpClass(cls):
        """
            Check if server is up and running before running any tests.
            Throws a ConnectionError when it can't reach said server.
        """
        r = http.get(urljoin(cls.uri, '/api/status'))
        print r.status_code, r.text
        assert http.get(urljoin(cls.uri, '/api/status')).status_code == 200, '/api/status not returning 200'

    def test_status(self):
        """ Not really needed, but whatever """
        status_resp = http.get(urljoin(self.uri, '/api/status'))
        for k in status_resp.json().keys():
            if k.endswith('_version'):
                self.assertEqual(status_resp[k].count('.'), 2)


if __name__ == '__main__':
    unittest_main()
