import pycurl
import io
import certifi
import urllib
import urllib.parse


class base_api:
    def __init__(self, key):
        self.api_key = key[0]
        self.bsecret = key[1].encode('utf-8')

    def initcurl(self, xtype):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.TIMEOUT, 15)
        # type: GET:0 POST:1 DELETE:2
        if xtype == 1:
            curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
        elif xtype == 2:
            curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        elif xtype == 0:
            curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
        return [curl, iofunc]

    def sort_params(self, params):
        p = dict(sorted(params.items(), key=lambda item: item[0]))
        return urllib.parse.urlencode(p)
