import http.server
import subprocess
import os
import threading

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Sert les fichiers depuis le dossier du site
        super().__init__(*args, directory="src/Chloé/Louvreescape", **kwargs)

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
        else:
            super().do_GET()

print("Serveur lancé → http://localhost:8080")
http.server.HTTPServer(("", 8080), Handler).serve_forever()
