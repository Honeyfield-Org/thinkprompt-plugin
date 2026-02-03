#!/usr/bin/env python3
"""
ThinkPrompt Device Authorization Flow

Handles the complete device auth flow:
1. Find free port
2. Request device code from API
3. Output user code for Claude to display
4. Open browser
5. Wait for callback with token
"""

import http.server
import socketserver
import socket
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import webbrowser
import os
import ssl

def get_ssl_context():
    """Get SSL context with proper certificate handling for all platforms."""
    # Try certifi first (most reliable, cross-platform)
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass

    # Default context uses system certificates
    # Works well on Windows and Linux, may fail on macOS
    ctx = ssl.create_default_context()

    # macOS/Linux: try common certificate locations as fallback
    if sys.platform != 'win32':
        cert_paths = [
            '/etc/ssl/cert.pem',
            '/etc/ssl/certs/ca-certificates.crt',
            '/usr/local/etc/openssl/cert.pem',
            '/usr/local/etc/openssl@1.1/cert.pem',
        ]

        for path in cert_paths:
            if os.path.exists(path):
                try:
                    ctx.load_verify_locations(path)
                    return ctx
                except Exception:
                    continue

    return ctx

def find_free_port():
    """Find an available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def request_device_code(api_url: str, redirect_uri: str) -> dict:
    """Request a device code from the API."""
    url = f"{api_url}/auth/device"
    data = json.dumps({"redirectUri": redirect_uri}).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        ctx = get_ssl_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handle the OAuth callback."""

    result = {"status": "pending", "token": None, "error": None}

    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/callback':
            token = params.get('token', [None])[0]
            status = params.get('status', [None])[0]

            if status == 'complete' and token:
                CallbackHandler.result = {"status": "complete", "token": token}
                html = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>ThinkPrompt</title></head>
<body style="font-family:system-ui;text-align:center;padding:50px;background:#f5f5f5">
<div style="background:white;padding:40px;border-radius:12px;max-width:400px;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.1)">
<h1 style="color:#22c55e;margin:0 0 16px">✓ Erfolgreich!</h1>
<p style="color:#666;margin:0">Du kannst dieses Fenster schließen und zu Claude Code zurückkehren.</p>
</div></body></html>'''
            else:
                error = params.get('error', ['Unbekannter Fehler'])[0]
                CallbackHandler.result = {"status": "error", "error": error}
                html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>ThinkPrompt</title></head>
<body style="font-family:system-ui;text-align:center;padding:50px;background:#f5f5f5">
<div style="background:white;padding:40px;border-radius:12px;max-width:400px;margin:0 auto;box-shadow:0 2px 8px rgba(0,0,0,0.1)">
<h1 style="color:#ef4444;margin:0 0 16px">✗ Fehlgeschlagen</h1>
<p style="color:#666;margin:0">{error}</p>
</div></body></html>'''

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

def wait_for_callback(port: int, timeout: int = 300) -> dict:
    """Start server and wait for callback."""
    socketserver.TCPServer.allow_reuse_address = True

    try:
        httpd = socketserver.TCPServer(("127.0.0.1", port), CallbackHandler)
        httpd.socket.settimeout(timeout)
        httpd.handle_request()
        httpd.server_close()
        return CallbackHandler.result
    except socket.timeout:
        return {"status": "error", "error": "timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    # Get API URL from environment or use default
    api_url = os.environ.get(
        'THINKPROMPT_API_URL',
        'https://thinkprompt-api-v2.azurewebsites.net/api/v1'
    )

    # Step 1: Find free port
    port = find_free_port()
    redirect_uri = f"http://localhost:{port}/callback"

    # Step 2: Request device code
    response = request_device_code(api_url, redirect_uri)

    if "error" in response:
        print(f"ERROR={response['error']}")
        print("STATUS=error")
        sys.exit(1)

    # Extract data
    data = response.get('data', response)
    user_code = data.get('userCode')
    verification_uri = data.get('verificationUri', '')

    if not user_code:
        print("ERROR=No user code received")
        print("STATUS=error")
        sys.exit(1)

    # Step 3: Output user code (Claude will display this)
    print(f"USER_CODE={user_code}")

    # Step 4: Determine verification URL
    if 'localhost' in api_url:
        verify_url = f"http://localhost:3002/device?code={user_code}"
    else:
        verify_url = f"{verification_uri}?code={user_code}" if verification_uri else f"https://thinkprompt.app/device?code={user_code}"

    print(f"VERIFY_URL={verify_url}")

    # Step 5: Open browser
    webbrowser.open(verify_url)
    print("BROWSER=opened")

    # Step 6: Wait for callback
    result = wait_for_callback(port)

    if result["status"] == "complete":
        print(f"TOKEN={result['token']}")
        print("STATUS=complete")
    else:
        print(f"ERROR={result.get('error', 'unknown')}")
        print("STATUS=error")
        sys.exit(1)

if __name__ == "__main__":
    main()
