from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PORT = int(os.environ.get("PORT", 5173))
INDEX_PATH = os.path.join(os.path.dirname(__file__), "index.html")

MOCK_RESPONSE = {
    "proposals": [
        {
            "title": "Cozy Alpine Reset",
            "description": "A calm, scenic week with light walks, warm cafes, and charming villages.",
            "highlights": [
                "4–5 nights in a walkable alpine town",
                "Easy day trips with scenic rail views",
                "One special dinner with local flavors",
            ],
        },
        {
            "title": "Seaside Wellness Escape",
            "description": "Gentle ocean breezes, slow mornings, and relaxed coastal exploration.",
            "highlights": [
                "Beachfront hotel with spa access",
                "Sunset strolls and markets",
                "Short sightseeing loop with flexible pacing",
            ],
        },
        {
            "title": "City + Countryside Balance",
            "description": "A cultural city base paired with a restful countryside retreat.",
            "highlights": [
                "2 nights in the city for museums and food",
                "3–4 nights in a quiet village",
                "Private transfer or scenic train between",
            ],
        },
    ]
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            try:
                with open(INDEX_PATH, "rb") as f:
                    self._send(200, "text/html", f.read())
            except OSError:
                self._send(500, "text/plain", "Failed to load index.html")
            return
        self._send(404, "text/plain", "Not found")

    def do_POST(self):
        if self.path == "/api/travel-proposals":
            _ = self.rfile.read(int(self.headers.get("Content-Length", "0") or "0"))
            self._send(200, "application/json", json.dumps(MOCK_RESPONSE))
            return
        self._send(404, "text/plain", "Not found")


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"Mock server running at http://localhost:{PORT}")
    server.serve_forever()
