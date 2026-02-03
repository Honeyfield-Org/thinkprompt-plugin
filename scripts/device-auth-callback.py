#!/usr/bin/env python3
"""ThinkPrompt Device Authorization - Callback Server Only"""

import http.server
import socketserver
import socket
import sys

RESULT = {"status": "pending", "token": None, "error": None}

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global RESULT
        import urllib.parse
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/callback':
            token = params.get('token', [None])[0]
            status = params.get('status', [None])[0]

            if status == 'complete' and token:
                RESULT = {"status": "complete", "token": token}
                html = '<html><body style="font-family:system-ui;text-align:center;padding:50px"><h1>Erfolgreich!</h1><p>Du kannst dieses Fenster schliessen.</p></body></html>'
            else:
                RESULT = {"status": "error", "error": params.get('error', ['unknown'])[0]}
                html = '<html><body style="font-family:system-ui;text-align:center;padding:50px"><h1>Fehlgeschlagen</h1></body></html>'

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global RESULT

    if len(sys.argv) < 2:
        print("Usage: device-auth-callback.py <port>")
        print("STATUS=error")
        sys.exit(1)

    port = int(sys.argv[1])

    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), CallbackHandler)

    print(f"Waiting for callback on port {port}...")
    httpd.socket.settimeout(300)  # 5 min timeout

    try:
        httpd.handle_request()
    except socket.timeout:
        RESULT = {"status": "error", "error": "timeout"}
    except Exception:
        RESULT = {"status": "error", "error": "server_error"}
    finally:
        httpd.server_close()

    if RESULT["status"] == "complete":
        print(f"TOKEN={RESULT['token']}")
        print("STATUS=complete")
    else:
        print(f"ERROR={RESULT.get('error', 'timeout')}")
        print("STATUS=error")

if __name__ == "__main__":
    main()
