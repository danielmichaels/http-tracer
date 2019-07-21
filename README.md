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

```shell
pip install http-tracer
```

## Requirements

```shell
click==6.7
colorama==0.4.1
requests==2.21.0
```

Currently HTTP-Tracer is broken with anything newer than `click` 6.7 due to breaking changes within their API.

## Usage example

### Default output

![](/Examples/http-tracer-default.png?raw=True "http-tracer default output")

### Extended or Full output

```shell
http-tracer http://nyti.ms/1QETHgV --full 

  _  _ _   _            _                       
 | || | |_| |_ _ __ ___| |_ _ _ __ _ __ ___ _ _ 
 | __ |  _|  _| '_ \___|  _| '_/ _` / _/ -_) '_|
 |_||_|\__|\__| .__/    \__|_| \__,_\__\___|_|  
              |_|                              v 2019.7.1
    
[301] HTTP/1.1 GET http://nyti.ms/1QETHgV (625ms)  (cookies: 1)
[301] HTTP/1.1 GET http://trib.al/CPCEesg (606ms)  
[301] HTTP/1.1 GET http://nyti.ms/1Vsrnxp (283ms)  (cookies: 1)
[301] HTTP/1.1 GET http://bit.ly/1Vsrnxp?cc=af6dee160d88d673c6405cdf3785f1c8 (605ms)  (cookies: 1)
[301] HTTP/1.1 GET http://trib.al/YRVrqbr (386ms)  
[301] HTTP/1.1 GET http://nyti.ms/1QDeeSW (386ms)  
[301] HTTP/1.1 GET http://trib.al/HFpblHd (298ms)  
[301] HTTP/1.1 GET http://www.nytimes.com/2016/01/27/nyregion/what-happened-to-jane-mayer-when-she-wrote-about-the-koch-brothers.html?smid=tw-nytimes&smtyp=cur (97ms)  (cookies: 1)
[200] HTTP/1.1 GET https://www.nytimes.com/2016/01/27/nyregion/what-happened-to-jane-mayer-when-she-wrote-about-the-koch-brothers.html?smid=tw-nytimes&smtyp=cur (183ms)  (cookies: 2)

HTTP-Tracer finished in 3473ms over 9 hops

[!]    START FULL OUTPUT       [!]

********* HOP NUMBER: 1 **********

##################################
             HEADERS              
##################################

Server: nginx
Date: Sat, 08 Sep 2018 04:29:32 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 109
Connection: keep-alive
Cache-Control: private, max-age=90
Location: http://trib.al/CPCEesg
Set-Cookie: _bit=i884tw-be8cfc26d277036c01-008; Domain=nyti.ms; Expires=Thu, 07 Mar 2019 04:29:32 GMT
Strict-Transport-Security: max-age=1209600

##################################
             COOKIES              
##################################

Cookie: _bit=i884tw-be8cfc26d277036c01-008; Domain=nyti.ms; Expires=Thu, 07 Mar 2019 04:29:32 GMT


##################################
             REDIRECTION              
##################################

Request for: https://www.nytimes.com/2016/01/27/nyregion/what-happened-to-jane-mayer-when-she-wrote-about-the-koch-brothers.html?smid=tw-nytimes&smtyp=cur
Redirected to http://trib.al/CPCEesg

********* HOP NUMBER: 2 **********

.. SNIP ..


!! FINAL DESTINATION !!
URL: https://www.nytimes.com/2016/01/27/nyregion/what-happened-to-jane-mayer-when-she-wrote-about-the-koch-brothers.html?smid=tw-nytimes&smtyp=cur
Status Code: 200

```

## Release History

**v 19.7.1**

- Update to `Click 7.0`
- Provide IP Address for each hop.
- Headers are coloured for easier reading.
- Users no longer need to enter `http://` or `https://` protocol.

**v 19.2.1**

- Pin `Click 6.7` due to breaking changes within its new API

**v 18.9.1**

- Stable release

**v 18.8.2rc1**

- Bug fixes

**v 18.8.1**

- Work in progress


## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Attribution & Motivation

This is a blatant python rip off of [Robin Wood](https://twitter.com/digininja) and [PaulSec's](https://github.com/PaulSec/HTTP-traceroute) previous work. 
Kudos to [Watson/http-traceroute](https://github.com/watson/http-traceroute) for his formatting and styling, check his great JS libraries!
