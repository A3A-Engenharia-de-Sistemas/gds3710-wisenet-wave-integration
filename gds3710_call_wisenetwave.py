from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests
import json
import time

from dotenv import load_dotenv

import os

load_dotenv()

NX_HOST = os.getenv("NX_HOST")
NX_USER = os.getenv("NX_USER")
NX_PASS = os.getenv("NX_PASS")
CAMERA_ID = os.getenv("CAMERA_ID")

token = None
token_expiration = 0

def authenticate():
    global token, token_expiration
    url = f"{NX_HOST}/rest/v3/login/sessions"
    payload = {
        "username": NX_USER,
        "password": NX_PASS,
        "setCookie": False
    }
    try:
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        token_expiration = time.time() + data.get("expiresInS")
        print("✅ Autenticado com sucesso no Nx Witness.")
    except Exception as e:
        print(f"❌ Falha na autenticação: {e}")

def send_event(source, caption, description):
    global token
    if token is None or time.time() >= token_expiration:
        authenticate()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "source": source,
        "caption": caption,
        "description": description,
        "metadata": json.dumps({"cameraRefs": [CAMERA_ID]}),
    }
    try:
        response = requests.post(f"{NX_HOST}/api/createEvent", headers=headers, json=payload, verify=False)
        response.raise_for_status()
        print(f"✅ Evento enviado: {caption} | {description} | Resposta: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao enviar evento: {e}")

class GDSProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data_raw = self.rfile.read(content_length).decode('utf-8')
        post_data = urllib.parse.parse_qs(post_data_raw)

        mac = post_data.get("mac", [""])[0]
        content = post_data.get("content", [""])[0]

        print(f"Recebido do GDS: MAC={mac} | Conteúdo={content}")

        if content != "Call Log(Door Bell Call)":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Ignorado")
            return

        send_event(source="GDS3710", caption="Interfone", description=content)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

if __name__ == "__main__":
    server_address = ('', 7777)
    httpd = HTTPServer(server_address, GDSProxyHandler)
    print("Servidor iniciado. Aguardando eventos do GDS na porta 7777...")
    httpd.serve_forever()
