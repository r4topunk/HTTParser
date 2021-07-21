# HTTParser
## About
HTTParser is a script that turns a raw HTTP request into a Python object.

## Usage
```python
from httparser import HttpRequest

HR = HttpRequest()
raw_request = """POST /something.php?foo=bar HTTP/1.1
Host: foo.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom"""

HR.set_raw_request(raw_request)
```

## Why I developed that?
Working in web app pentest with Burp Suite makes me deal with raw HTTP everyday. And I love work with Python, and with the requests lib. Whenever I create a new script, I need to separate the request with regex or something like that. So I decide to write a class where I can just paste my request and work with a object. With HTTParser I can change, add and remove the headers and cookies.

## Why "HTTParser"?
Yeah I know, that doesn't literally parse anything... But when I working on the script I needed to parse everything! And come on, the name is really cool!!!

## Help-me
If you can give my script a chance I'll be very happy!
Just paste a request on it and see what comes out.
Send me some types, or just ideas, or anything! Everything will be read with pleasure <3
