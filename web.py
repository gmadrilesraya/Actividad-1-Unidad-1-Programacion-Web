from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        # Esta línea causaba el error si get_response no estaba bien definida abajo
        contenido = self.get_response()
        
        if contenido is None:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write("<h1>404 - Pagina no encontrada</h1>".encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(contenido.encode("utf-8"))

def get_response(self):
    ruta = self.url().path
    query = self.query_data()

    if ruta == "/proyecto/web-uno":
        autor = query.get("autor", "Gerardo")
        return f"<h1>Proyecto: web-uno Autor: {autor}</h1>"

    return "Hola, sigo configurando el servidor..."

if __name__ == "__main__":
    puerto = 8000
    print(f"Servidor iniciado y escuchando en el puerto {puerto}...") 
    server = HTTPServer(("0.0.0.0", puerto), WebRequestHandler)
    server.serve_forever()