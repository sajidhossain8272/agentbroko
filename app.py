"""
Root entrypoint fallback for Vercel / WSGI / ASGI deployment.
"""
from api.index import app, handler

if __name__ == "__main__":
    import http.server
    server = http.server.HTTPServer(("", 8000), handler)
    print("Serving on http://localhost:8000")
    server.serve_forever()
