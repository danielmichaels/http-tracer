#!/usr/bin/env python

import requests


def main():
    Tracer('https://httpbin.org/redirect/4')


class Tracer:

    def __init__(self, url):
        self.url = url
        self.get_response()

    def get_response(self):
        resp = requests.get(self.url)
        return self.format_response(resp)

    def format_response(self, resp):
        if resp.history:
            for redirects in resp.history:
                self.template(status_code=redirects.status_code,
                              http_version=redirects.raw.version,
                              request_type=redirects.request.method,
                              url=redirects.url, time=redirects.elapsed,
                              cookies='cookies if any')
            print(resp.status_code, resp.request.method,
                  resp.url, resp.elapsed, 'cookies if any')
            print(f"Number of hops: {len(resp.history) +1}")

    def template(self, status_code, http_version, request_type, url, time, cookies):
        template = f"[{status_code}] HTTP/{http_version} {request_type} {url} {time} {cookies}"
        print(template)

    def time_converter(self, resp):
        """Parses request.elapsed into milliseconds"""
        pass

    def http_version_converter(self, resp):
        """Reformat requests raw.version integer into the HTTP header format"""
        pass

    def cookies_exist(self, resp):
        """Check if cookies sent during response."""
        pass


def args_parser():
    """
    should look like this:

    python http-tracer.py <url>

    <url> is a required argument

    which will call Tracer(<url>)
    :return:
    """
    pass


if __name__ == '__main__':
    main()
