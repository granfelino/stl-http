import logging
import http.server
import re
import json

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(module)s | %(levelname)s | %(message)s"
)

HOST = "localhost"
PORT = 8080
ADDRESS = (HOST, PORT)


class RequestHandler(http.server.BaseHTTPRequestHandler):
    __match_items = re.compile("^/items$")
    __match_items_id = re.compile(r"^/items/([a-zA-Z]+)$")
    _items = {"siema": "helo"}

    def items_to_json(self) -> bytes:
        return json.dumps(self._items).encode(encoding="utf-8")

    def list_items(self) -> None:
        self.send_response(200)
        items_s = self.items_to_json()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(items_s)))
        self.end_headers()
        self.wfile.write(items_s)

    def add_item(self, item_id: str, item_val: str) -> None:
        if item_id in self._items:
            self.send_response(404)
            body = f"Item with ID: {item_id} already exists."
            self.send_header("Context-Type", "plain/text")
            self.send_header("Context-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body.encode(encoding="utf-8"))
        else:
            self.send_response(200)
            self.send_header("Context-Type", "text/plain")
            self.send_header("Context-Length", "0")
            self.end_headers()

            self._items[item_id] = item_val

    def list_single_item(self, item_id: str) -> None:
        item_s = self._items.get(item_id, None)

        if item_s is None:
            self.send_response(404)
            body = f"Item with ID: '{item_id}' not found.\n"
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body.encode(encoding="utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(item_s)))
            self.end_headers()
            self.wfile.write(item_s.encode(encoding="utf-8"))

    def invalid_request(self) -> None:
        self.send_response(404)
        body = "Page Not Found\n"
        self.send_header("Context-Type", "text/plain")
        self.send_header("Context-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body.encode(encoding="utf-8"))

    def do_GET(self):
        if self.__match_items.match(self.path):
            self.list_items()
        elif self.__match_items_id.match(self.path):
            item_id = self.__match_items_id.search(self.path).group(1)
            self.list_single_item(item_id)
        else:
            self.invalid_request()

    def do_POST(self):
        logging.info("POST request entry")

        path_cond = self.__match_items_id.match(self.path)
        logging.info(
            f"Path match of items/id: {path_cond}, with path being: {self.path}"
        )

        header_cond = (
            "Content-Length" in self.headers and int(self.headers["Content-Length"]) > 0
        )
        logging.info(f"Header check: {header_cond}")

        if path_cond and header_cond:
            item_id = self.__match_items_id.search(self.path).group(1)
            size = int(self.headers["Content-Length"])
            body = self.rfile.read(size)
            body_str = body.decode()
            self.add_item(item_id, body_str)
        else:
            self.invalid_request()


def main():
    httpd = http.server.HTTPServer(ADDRESS, RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
