#!/usr/bin/env python

import click
import requests
from colorama import Fore as fg
from colorama import Style as sty


@click.command()
@click.argument('url')
@click.option('--full', '-f', is_flag=True,
              help='Do a full scan of the redirect chain.')
def main(url, full):
    tracer = Tracer(url)
    resp = tracer.get_response()
    tracer.format_response(resp)
    if full:
        full_tracer = FullTracer(url)
        full_tracer.run(resp)


class Tracer:
    """Parent class that gets the url response, and contains the helper methods
    for cleaning up the formatting."""

    def __init__(self, url):
        self.url = url
        self.get_response()

    def get_response(self):
        try:
            resp = requests.get(self.url)
            if resp.status_code == 200:
                return resp
            else:
                raise ConnectionError

        except requests.ConnectionError or requests.ConnectTimeout as e:
            click.secho(f"{e} Caused Fatal Error!", blink=True, fg='red')
        except requests.HTTPError as e:
            click.secho(f"{e} Caused Fatal Error!", blink=True, fg='red')

    def template(self, status_code, http_version, request_type, url, time,
                 cookies):
        template = f"{fg.GREEN}[{status_code}]{fg.YELLOW} HTTP/{http_version}" \
                   f" {fg.BLUE}{request_type} {fg.WHITE}{url} {fg.CYAN}({time}ms)" \
                   f" {fg.LIGHTGREEN_EX} {cookies or ''}{sty.RESET_ALL}"
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
        print(
            f"\n{fg.WHITE}HTTP-Tracer finished in {fg.CYAN}{self.total_time_elapsed(resp)}ms{fg.WHITE} over"
            f"{fg.CYAN} {len(resp.history) + 1}{fg.WHITE} hops{sty.RESET_ALL}")


class FullTracer(Tracer):
    """Full output that presents headers, cookies, cert validation/ expiry."""

    def run(self, resp):
        data = self.create_dicts(resp)
        self.full_format(data, resp)

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

    def full_format(self, header_list, resp):

        print()
        hop = 0
        print(f"{fg.WHITE}[!]    START FULL OUTPUT       [!]{sty.RESET_ALL}")
        for dict_item in header_list:
            hop += 1
            print()
            click.secho("##################################", fg='yellow')
            print("             HEADERS              ")
            click.secho("##################################", fg='yellow')
            click.secho(f"    [*]hop number: {hop}[*]", fg='white')
            print()

            for k, v in dict_item.items():
                # unordered dict.
                print(f"{fg.WHITE}{k}: {sty.RESET_ALL}{v}")

            print()
            if 'Set-Cookie' in dict_item.keys():
                click.secho("##################################", fg='green')
                print("             COOKIES              ")
                click.secho("##################################", fg='green')
                print(f"Cookie: {dict_item['Set-Cookie']}")
                print()

            if 'Location' in dict_item.keys():
                print()
                click.secho("##################################", fg='blue')
                print("             REDIRECTION              ")
                click.secho("##################################", fg='blue')
                click.secho(f"Redirected to: {dict_item['Location']}",
                            fg='white')

        print()
        click.secho(f"Final URL: {resp.url} [{resp.status_code}]",
                    fg='magenta')


if __name__ == '__main__':
    main()
