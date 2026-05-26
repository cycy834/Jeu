import http.server
import subprocess
import os
import threading

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Sert les fichiers depuis le dossier du site
        super().__init__(*args, directory="src/Chloé/presentationsite", **kwargs)

    def do_GET(self):
        if self.path == "/launch":
            # Lance le jeu dans un thread séparé
            threading.Thread(target=lambda: subprocess.Popen(
                ["python3", "main.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )).start()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        elif self.path == "/":
            self.path = "/pres.html"
            super().do_GET()
        else:
            super().do_GET()
    def handle_error(self, request, client_address):
        pass
print("Serveur lancé → http://localhost:8081")
http.server.HTTPServer(("", 8081), Handler).serve_forever()
