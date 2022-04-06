# -*- coding: utf-8 -*-

# Generic/Built-in
from http.client import InvalidURL
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import uuid
import webbrowser

# ammaraskar/pyCraft
from minecraft.authentication import AuthenticationToken, Profile

# JakobDev/minecraft-launcher-lib
from minecraft_launcher_lib.microsoft_account import complete_login

class _S(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.server.auth_code = parse_qs(urlparse(self.path).query).get('code', None)[0]
        if not self.server.auth_code:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"Something went wrong. The following path did not contain any auth code: {self.path}".encode("utf8"))
            raise InvalidURL
        
        self.wfile.write(f"Successfully authenticated. You can close this window now.".encode("utf8"))

    def log_message(self, format, *args):
        pass

def authenticate(client_id: str, client_secret, redirect_port: int) -> AuthenticationToken:
    redirect_uri = f'http://localhost:{redirect_port}'

    login_url = f'https://login.live.com/oauth20_authorize.srf?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=XboxLive.signin%20offline_access'
    webbrowser.open(login_url, new=0, autoraise=True)

    httpd = HTTPServer(('', redirect_port), _S)
    
    httpd.handle_request()

    if not hasattr(httpd, 'auth_code'):
        raise TimeoutError

    login_data = complete_login(client_id, client_secret, redirect_uri, httpd.auth_code)

    auth_token = AuthenticationToken(username=login_data['name'], access_token=login_data['access_token'], client_token=uuid.uuid4().hex)
    auth_token.profile = Profile(id_=login_data['id'], name=login_data['name'])
    return auth_token