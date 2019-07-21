#!/usr/bin/env python
import random
import re
import socket
import sys

import click
import requests
from colorama import Fore as fg
from colorama import Style as sty
from tld import get_fld

version = "2019.7.1"


@click.command()
@click.argument("url")
@click.option(
    "--full",
    "-f",
    multiple=True,
    is_flag=True,
    help="Print detailed report on each hop along the path",
)
def main(url, full):
    """
    HTTP-Tracer returns the redirects on way to the destination URL.

    If user does not supply 'https://' it will default to 'http://'
    """
    tracer = Tracer(url)
    resp = tracer.get_response()
    tracer.format_response(resp)
    if full:
        full_tracer = FullTracer(url)
        full_tracer.run(resp)


class Tracer:
    """
    Parent class that gets the url response, and contains the helper methods
    for cleaning up the formatting.
    """

    logo = f"""{fg.WHITE}
  _  _ _   _            _                       
 | || | |_| |_ _ __ ___| |_ _ _ __ _ __ ___ _ _ 
 | __ |  _|  _| '_ \___|  _| '_/ _` / _/ -_) '_|
 |_||_|\__|\__| .__/    \__|_| \__,_\__\___|_|  
              |_|                              v {version}{sty.RESET_ALL}
    """

    def __init__(self, url):
        self.url = url
        self.get_response()

    @staticmethod
    def user_agent():
        user_agents = [
            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        ]
        agent = random.choice(user_agents)

        return agent

    def _http(self):
        """
        Prepend the URL with 'http://' if not added manually by the user.

        :return: http:// + url
        """
        if not re.match("(?:http|https)://", self.url):
            return f"http://{self.url}"
        return self.url

    def get_response(self):
        """
        Gets the response object for the URL specified.

        :returns: response object
        """
        try:
            resp = requests.get(self._http(), headers={"User-Agent": self.user_agent()})
            return resp
        except requests.exceptions.MissingSchema or requests.exceptions.InvalidSchema as e:
            click.echo(
                f"Schema Error. Only 'http://' and 'https://' supported\n{e}\nExiting..."
            )
            sys.exit(1)
        except ConnectionError as e:
            click.echo(f"Error Occurred!\n{e}\nExiting...")
            sys.exit(1)
        except requests.ConnectionError or requests.ConnectTimeout as e:
            click.echo(f"Error Occurred!\n{e}\nExiting...")
            sys.exit(1)
        except requests.HTTPError as e:
            click.echo(f"Error Occurred!\n{e}\nExiting...")
            sys.exit(1)

    @staticmethod
    def time_converter(resp):
        """
        Parses request.elapsed into milliseconds

        :param resp: response object
        :returns: integer that represents milliseconds

        """
        return int(resp.total_seconds() * 1000)

    @staticmethod
    def http_version_converter(resp):
        """
        Reformat requests raw.version integer into the HTTP header format

        :param resp: response object
        :returns: either 1.1 or 2 for http version
        """
        if len(str(resp)) > 1:
            resp = [x for x in str(resp)]
            return f"{resp[0]}.{resp[1]}"
        else:
            return resp

    @staticmethod
    def total_time_elapsed(resp):
        """
        Return the total time taken for all redirects.

        :param resp: response object
        :returns: sum of all response times in milliseconds.
        """
        total = list()
        for redirects in resp.history:
            tt = redirects.elapsed.total_seconds()
            total.append(tt)
        total.append(resp.elapsed.total_seconds())
        return int(sum(total) * 1000)

    @staticmethod
    def cookies_exist(resp):
        """
        Check if cookies sent during response.

        :param resp: response object.
        :returns: dictionary of cookies from response if exists or None.
        """
        if not resp.cookies.get_dict():
            return
        else:
            cookies = resp.cookies.get_dict()
            if len(cookies) >= 1:
                return f"(cookies: {len(cookies)})"

    @staticmethod
    def _ipaddr(url):
        url = get_fld(url)
        try:
            return socket.gethostbyname(url)
        except AttributeError as e:
            click.echo(e)

    def template(
        self, status_code, http_version, request_type, url, time, cookies, ipaddr
    ):
        """Method for templating the responses."""
        template = (
            f"{fg.GREEN}[{status_code}]{fg.YELLOW} HTTP/{http_version}"
            f" {fg.BLUE}{request_type}{fg.RED} {ipaddr} {fg.WHITE}{url} {fg.CYAN}({time}ms)"
            f" {fg.LIGHTGREEN_EX} {cookies or ''}{sty.RESET_ALL} "
        )
        print(template)

    def format_response(self, resp):
        """The default output for HTTP-Tracer."""
        print(self.logo)
        if resp.history:

            for redirects in resp.history:
                self.template(
                    status_code=redirects.status_code,
                    http_version=self.http_version_converter(redirects.raw.version),
                    request_type=redirects.request.method,
                    url=redirects.url,
                    time=self.time_converter(redirects.elapsed),
                    cookies=self.cookies_exist(redirects),
                    ipaddr=self._ipaddr(redirects.url),
                )
        self.template(
            resp.status_code,
            self.http_version_converter(resp.raw.version),
            resp.request.method,
            resp.url,
            self.time_converter(resp.elapsed),
            self.cookies_exist(resp),
            self._ipaddr(resp.url),
        )
        if resp.status_code == 404:
            print(
                f"\n{fg.WHITE}HTTP-Tracer Returned {fg.RED}404{sty.RESET_ALL}{fg.WHITE}"
                f" in {fg.CYAN}{self.total_time_elapsed( resp)}ms{fg.WHITE} over"
                f"{fg.CYAN} {len( resp.history) + 1}{fg.WHITE} hops{sty.RESET_ALL}"
            )

        else:
            print(
                f"\n{fg.WHITE}HTTP-Tracer finished in {fg.CYAN}{self.total_time_elapsed( resp)}ms{fg.WHITE} over"
                f"{fg.CYAN} {len( resp.history) + 1}{fg.WHITE} hops{sty.RESET_ALL}"
            )


class FullTracer(Tracer):
    """Full output that presents headers, cookies and redirect urls."""

    def run(self, resp):
        """Helper method that calls the other methods within FullTracer."""
        data = self.create_dicts(resp)
        self.full_format(data, resp)

    @staticmethod
    def create_dicts(resp):
        """
        Returns a list of dictionaries of all response headers.

        :param resp: response object
        :returns: list of dictionaries containing response headers.
        """
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
        """
        A method that iterates over a list of dictionaries, and the response
        object. Used in the --full (-f) option when running the application.

        :param header_list: list of dictionaries containing header info.
        :param resp: response object.
        """

        print()
        hop = 0
        print(f"{fg.WHITE}[!]    START FULL OUTPUT       [!]{sty.RESET_ALL}")
        for dict_item in header_list:
            hop += 1
            print()
            click.secho(f"********* HOP NUMBER: {hop} **********", fg="magenta")
            print()
            click.secho("##################################", fg="yellow")
            print("             HEADERS              ")
            click.secho("##################################", fg="yellow")
            print()

            for k, v in dict_item.items():
                # unordered dict.
                print(f"{fg.LIGHTCYAN_EX}{k}: {sty.RESET_ALL}{v}")

            print()
            if "Set-Cookie" in dict_item.keys():
                click.secho("##################################", fg="green")
                print("             COOKIES              ")
                click.secho("##################################", fg="green")
                print()
                print(
                    f"{fg.LIGHTCYAN_EX}Cookie:{sty.RESET_ALL} {dict_item[ 'Set-Cookie']}"
                )
            print()

            if "Location" in dict_item.keys():
                print()
                click.secho("##################################", fg="blue")
                print("             REDIRECTION              ")
                click.secho("##################################", fg="blue")
                print()
                print(f"{fg.LIGHTCYAN_EX}Request for:{sty.RESET_ALL} {resp.url}")
                print(
                    f"{fg.LIGHTCYAN_EX}Redirected to: {dict_item['Location']}{fg.RED} => {sty.RESET_ALL} {self._ipaddr(resp.url)} "
                )

        print(f"{fg.YELLOW}!! FINAL DESTINATION !!")
        print(f"{fg.WHITE}[200 OK] {sty.RESET_ALL} {resp.url}")
        print(f"{fg.WHITE}IP Address:{sty.RESET_ALL} {self._ipaddr(resp.url)}")


if __name__ == "__main__":
    main()
