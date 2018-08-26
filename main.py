#!/usr/bin/env python

import requests


def main():
    BasicTracer('https://httpbin.org/redirect/4')


class Tracer:
    """Parent class that gets the url response, and contains the helper methods
    for cleaning up the formatting."""

    def __init__(self, url):
        self.url = url
        self.get_response()

    def get_response(self):
        resp = requests.get(self.url)
        return self.format_response(resp)

    def template(self, status_code, http_version, request_type, url, time,
                 cookies):
        template = f"[{status_code}] HTTP/{http_version} {request_type} {url} ({time}ms) ({cookies} found)"
        print(template)

    def time_converter(self, resp):
        """Parses request.elapsed into milliseconds"""
        return int(resp.total_seconds() * 1000)

    def http_version_converter(self, resp):
        """Reformat requests raw.version integer into the HTTP header format"""
        if len(str(resp)) > 1:
            resp = [x for x in str(resp)]
            return f"{resp[0]}.{resp[1]}"
        else:
            return resp

    def total_time_elapsed(self, resp):
        """Return the total time taken for all redirects."""
        total = list()
        for redirects in resp.history:
            tt = redirects.elapsed.total_seconds()
            total.append(tt)
        total.append(resp.elapsed.total_seconds())
        return int(sum(total) * 1000)

    def cookies_exist(self, resp):
        """Check if cookies sent during response."""
        pass


class BasicTracer(Tracer):
    """The basic output of http-tracer."""
    def format_response(self, resp):
        if resp.history:
            for redirects in resp.history:
                self.template(status_code=redirects.status_code,
                              http_version=self.http_version_converter(redirects.raw.version),
                              request_type=redirects.request.method,
                              url=redirects.url, time=self.time_converter(redirects.elapsed),
                              cookies='cookies if any')
            print(resp.status_code, resp.request.method, resp.raw.version,
                  resp.url, resp.elapsed, 'cookies if any')
            print(f"Number of hops: {len(resp.history) +1} and took {self.total_time_elapsed(resp)}ms")


class FullTracer(Tracer):
    """Full output that presents headers, cookies, cert validation/ expiry."""
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
