import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from entries import get_all_entries
from entries import get_single_entry



class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)
        if len(parsed) == 2:
            ( resource, id ) = parsed
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
        # elif len(parsed) == 3:
        #     ( resource, key, value ) = parsed
        #     # Is the resource `customers` and was there a
        #     # query parameter that specified the customer
        #     # email as a filtering value?
        #     if key == "email" and resource == "customers":
        #         response = get_customers_by_email(value)
        #     elif key == "location_id" and resource == "animals":
        #         response = get_animals_by_location(value)
        #     elif key == "location_id" and resource == "employees":
        #         response = get_employees_by_location(value)
        #     elif key == "status" and resource == "animals":
        #         response = get_animals_by_status(value)
        self.wfile.write(response.encode())


    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        new_entry = None

        if resource == "entries":
            new_entry = create_entry(post_body)
            self.wfile.write(f"{new_entry}".encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        if resource == "entries":
            update_entry(id, post_body)
        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        if resource == "entries":
            delete_entry(id)
        self.wfile.write("".encode())


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
