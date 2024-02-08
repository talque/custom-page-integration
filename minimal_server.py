#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse, error
from typing import Dict, Any
import jwt
import logging
import json
import datetime

    
# Talque Credentials
api_client_id: str = '5sarR1DpXU7QJMDRdoKW'
api_client_secret: str = 'secret'


# Where the server is listening
hostname: str = 'localhost'
port: int = 9000


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
log = logging.getLogger('custom-page')


def get_token_from_path(path: str) -> str:
    log.debug('request path = {}'.format(path))
    parsed = parse.urlparse(path)
    log.debug('parsed path = {}'.format(parsed))
    qs = parse.parse_qs(parsed.query)
    log.debug('parsed query string = {}'.format(qs))
    token = qs['talque'][0]
    log.debug('extracted token = {}'.format(token))
    return token


def decode_jwt(token: str) -> Dict[str, Any]:
    decoded = jwt.decode(
        token,
        api_client_secret,
        algorithms=['HS256'],
        options=dict(
            verify_aud=False,
            verify_signature=True,
        ),
    )
    log.debug('decoded jwt = {}'.format(decoded))
    return decoded


HTML = """
<html>
<head>
    <title>Custom page integration</title>
</head>
<body>
    <h1>Custom Page Integration</h1>

    <p>
        This is an example backend service that generates a user-specific
        page for embedding as an iframe in talque
    </p>
 
    <p style="word-wrap: break-word;">
        You accessed url path: {path}
    </p>

    <p>
       The signed Json Web Token payload is
    </p>

    <pre>{pre}</pre>

    <p>
       The JWT contains the following information:
    </p>

    <ul>
        <li>org id = {org_id}</li>
        <li>talque profile id = {profile_id}</li>
        <li>external org id, if known = {ext_org_id}</li>
        <li>external user id, if known = {ext_user_id}</li>
        <li>token expires at {expires}</li>
    </ul>

</body>
</html>
"""


class RequestHandler(BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.0'
    error_content_type = 'text/plain'
    error_message_format = "Error %(code)d: %(message)s"

    def html(self) -> str:
        encoded = get_token_from_path(self.path)
        decoded = decode_jwt(encoded)
        expires = datetime.datetime.fromtimestamp(decoded['exp'], datetime.UTC)
        return HTML.format(
            path=self.path,
            jwt=decoded,
            pre=json.dumps(decoded, indent=4),
            org_id=decoded['aud'],
            profile_id=decoded['sub'],
            ext_org_id=decoded['eventId'],
            ext_user_id=decoded['extId'],
            expires=expires,
        )
    
    def do_GET(self):
        print(self.request)
        try:
            html = self.html()
        except Exception as error:
            log.exception(error)
            self.send_error(400, repr(error))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))


def serve(hostname: str, port: int):
    server_address = (hostname, port)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()

    
if __name__ == '__main__':
    log.info(f'Use http://{hostname}:{port}/?talque={api_client_id} as your talque custom page iframe url')
    serve(hostname, port)
    
