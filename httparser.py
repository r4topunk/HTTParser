from urllib.parse import urlparse, parse_qs, unquote


class HttpRequest:
    """ Creat an object from an HTTP request """
    def __init__(self, raw_request=None):
        self.headers = {}
        self.parameters = {}
        self.cookies = {}

        if raw_request:
            self.set_raw_request(raw_request)

    # SETTERS
    def set_headers(self, req_top):
        for header_line in req_top:
            header_key, header_value = header_line.split(": ", 1)
            if header_key == "Cookie":
                for cookie in header_value.split(";"):
                    cookie_name, cookie_value = cookie.strip().split("=", 1)
                    self.add_cookie(cookie_name, cookie_value)
            else:
                self.add_header(header_key, header_value)

    def set_header_value(self, key, value):
        self.headers[key] = value

    def set_parameters(self, query_string):
        for param_key, param_value in query_string.items():
            self.add_parameter(param_key, param_value[0])

    def set_param_value(self, key, value):
        self.parameters[key] = value

    def set_url(self, url):
        self.url = url

    def set_query_string_url(self):
        self.query_string_url = self.url + f"?{self.get_query_string()}"

    def set_body(self, body=None):
        self.body = body

    def set_path(self, path):
        self.path = path

    def set_verb(self, verb):
        self.verb = verb

    def set_http_version(self, http_version):
        self.http_version = http_version

    def set_raw_request(self, raw_request):
        # Removes any adicional line break
        raw_request = raw_request.strip()
        http_verbs = ["GET", "POST", "PUT", "DELETE", "TRACE"]
        if raw_request.split(" ", 1)[0] not in http_verbs:
            exit("Invalid request")

        # Separates the request body
        request = raw_request.split("\n\n", 1)
        req_top = [lines.strip() for lines in request[0].splitlines()]

        try:
            req_body = request[1]
        except IndexError:
            # The request was pasted without body
            req_body = ""

        self.set_body(req_body)
        self.set_headers(req_top[1:])

        # First line be like: POST /something?foo=bar HTTP/2.0
        req_first_line = req_top[0].split(" ")
        self.set_verb(req_first_line[0])
        self.set_http_version(req_first_line[2].split("/")[1])

        req_path_and_params = req_first_line[1]
        url = f"https://{self.get_header('Host')}{req_path_and_params}"
        parsed_url = urlparse(url)
        self.set_url(parsed_url.geturl())
        self.set_path(parsed_url.path)
        self.set_parameters(parse_qs(parsed_url.query))
        self.set_query_string_url()

    # GETTERS
    def get_url(self):
        return self.url

    def get_query_string_url(self):
        return self.query_string_url

    def get_body(self):
        return self.body

    def get_cookies(self):
        return self.cookies

    def get_headers(self):
        return self.headers

    def get_header(self, header_name):
        return self.headers[header_name]

    def get_parameters(self):
        return self.parameters

    def get_parameter(self, param_name):
        return self.parameters[param_name]

    def get_path(self):
        return self.path

    def get_verb(self):
        return self.verb

    def get_http_version(self):
        return self.http_version

    def get_request(self, unquote=False):
        request = f"{self.get_verb()} "
        request += f"{self.get_path()}"
        request += f"{self.get_query_string()} "
        request += f"HTTP/{self.get_http_version()}\n"

        for header_key, header_value in self.get_headers().items():
            request += f"{header_key}: {header_value}\n"

        request += "Cookie: "
        enum_cookie = enumerate(self.get_cookies().items())
        for index, cookie in enum_cookie:
            cookie_key, cookie_value = cookie
            request += f"{cookie_key}={cookie_value}"
            if index != (len(self.get_cookies()) - 1):
                request += "; "

        request += "\n\n"

        if unquote is True:
            request += unquote(self.get_body())
        else:
            request += self.get_body()

        return request

    def get_query_string(self):
        if len(self.get_parameters()) > 1:
            param_line = "?"
            for param_key, param_value in self.get_parameters().items():
                param_line += f"{param_key}={param_value}&"
            param_line = param_line.rstrip("&")
            return param_line
        else:
            return ""

    # ADDERS
    def add_cookie(self, name, value):
        self.cookies[name] = value

    def add_header(self, key, value):
        self.headers[key] = value

    def add_parameter(self, key, value):
        self.parameters[key] = value

    # DELETERS
    def del_cookie(self, name):
        del self.cookies[name]

    def del_header(self, name):
        del self.headers[name]

    def del_parameter(self, name):
        del self.parameters[name]
