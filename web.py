from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
from rutas import rutas_del_sitio
import os

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
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

        if ruta in rutas_del_sitio:
            valor = rutas_del_sitio[ruta]

            if isinstance(valor, str) and valor.endswith(".html"):
                if os.path.exists(valor):
                    with open(valor, "r", encoding="utf-8") as f:
                        return f.read()
                else:
                    return f"<h1>Error: El archivo '{valor}' no se encuentra en la carpeta</h1>"

            if "{autor}" in valor:
                autor = query.get("autor", "Gerardo")
                return valor.format(autor=autor)

            return valor

        return None

if __name__ == "__main__":
    puerto = 8000
    print(f"Servidor iniciado y escuchando en el puerto {puerto}...") 
    server = HTTPServer(("0.0.0.0", puerto), WebRequestHandler)
    server.serve_forever()