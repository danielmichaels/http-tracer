#!/usr/bin/env python

import click
import requests


@click.command()
@click.argument('url')
@click.option('--full', '-f', is_flag=True,
              help='Do a full scan of the redirect chain.')
def main(url, full):
    tracer = Tracer(url)
    resp = tracer.get_response()
    if full:
        full_tracer = FullTracer(url)
        full_tracer.format_response(resp)
        full_tracer.run(resp)
    else:
        tracer.format_response(resp)
    # BasicTracer('https://httpbin.org/redirect/4')
    # BasicTracer('http://nyti.ms/1QETHgV')  # many redirects


class Tracer:
    """Parent class that gets the url response, and contains the helper methods
    for cleaning up the formatting."""

    def __init__(self, url):
        self.url = url
        self.get_response()

    def get_response(self):
        resp = requests.get(self.url)
        # return self.format_response(resp)
        return resp

    def template(self, status_code, http_version, request_type, url, time,
                 cookies):
        template = f"[{status_code}] HTTP/{http_version} {request_type} {url} ({time}ms) {cookies or ''}"
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
        if not resp.cookies.get_dict():
            return
        else:
            cookies = resp.cookies.get_dict()
            if len(cookies) >= 1:
                return f"(cookies: {len(cookies)})"

    def format_response(self, resp):
        if resp.history:
            for redirects in resp.history:
                self.template(status_code=redirects.status_code,
                              http_version=self.http_version_converter(
                                  redirects.raw.version),
                              request_type=redirects.request.method,
                              url=redirects.url,
                              time=self.time_converter(redirects.elapsed),
                              cookies=self.cookies_exist(redirects))
            self.template(resp.status_code,
                          self.http_version_converter(resp.raw.version),
                          resp.request.method,
                          resp.url, self.time_converter(resp.elapsed),
                          self.cookies_exist(resp))
        print(f"HTTP-Tracer finished in {self.total_time_elapsed(resp)}ms over"
              f" {len(resp.history) + 1} hops")


class FullTracer(Tracer):
    """Full output that presents headers, cookies, cert validation/ expiry."""

    def run(self, resp):
        data = self.create_dicts(resp)
        # print('list item: {}\n'.format([d for d in data]))
        self.full_format(data)

    def create_dicts(self, resp):
        list_of_headers = list()
        if resp.history:
            last_header = dict()
            for redirects in resp.history:
                redirected_headers = dict()
                for k, v in redirects.headers.items():
                    redirected_headers[k] = v
                list_of_headers.append(redirected_headers)
            for k, v in resp.headers.items():
                last_header[k] = v
            list_of_headers.append(last_header)

        return list_of_headers

    def full_format(self, header_list):

        print()
        for items in header_list:
            # print(items)

            print("##################################")
            print("             HEADERS              ")
            print("##################################")
            print()
            for k, v in items.items():
                print("{}:    {}".format(k, v))

        # cookies

        # redirection


if __name__ == '__main__':
    main()
