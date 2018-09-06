```
  _  _ _   _            _                       
 | || | |_| |_ _ __ ___| |_ _ _ __ _ __ ___ _ _ 
 | __ |  _|  _| '_ \___|  _| '_/ _` / _/ -_) '_|
 |_||_|\__|\__| .__/    \__|_| \__,_\__\___|_|  
 
```
# HTTP-Tracer
> A python script for ascertaining the redirection path taken when accessing a URL

HTTP-Tracer takes a URL and returns all redirects.
It will report the status code of each hop, and time taken to get its response. HTTP-Tracer
by default returns a simple output to quickly ascertain the number of hops. Given the `--full`
flag, it will return all the headers, cookies and redirects for each hop. 


## Installation

```sh
pip install http-traceroute
```


## Usage example

```shell
http-tracer http://nyti.ms/1QETHgV
```
**insert pic**


```shell
http-tracer http://nyti.ms/1QETHgV --full # (or -f)
```
**insert pic**


## Release History

v 18.8.1
    * Work in progress


## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Attribution & Motivation

Robin Wood @digininja and PaulSec. This is a blatant python rip off of their
great work. Check them out.

Watson/http-tracer for his formatting and styling. Check his great JS libraries!
