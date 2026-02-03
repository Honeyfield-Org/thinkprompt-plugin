---
description: Configure ThinkPrompt API credentials using Device Authorization Flow
---

# ThinkPrompt Plugin Setup (Device Authorization Flow)

You are helping the user configure their ThinkPrompt API credentials using the Device Authorization Flow (RFC 8628).

## Step 1: Check Existing Configuration

First, check if there's already an API key configured:

1. Read the file `~/.claude/settings.json`
2. If it exists and contains `env.THINKPROMPT_API_KEY`:
   - Try to validate it by calling any ThinkPrompt MCP tool (e.g., `mcp__plugin_thinkprompt_thinkprompt__list_workspaces`)
   - If the call succeeds: Tell the user "ThinkPrompt ist bereits konfiguriert und funktioniert!" and exit
   - If the call fails: The key is invalid, continue with Step 2

If no key exists or validation failed, continue with Step 2.

## Step 2-4: Run Device Auth Script (Local Callback Server)

Run the following Python script that handles everything: starts a local callback server, initiates device auth, opens the browser, and waits for the callback:

```bash
python3 << 'DEVICEAUTH'
import http.server
import socketserver
import socket
import json
import urllib.request
import urllib.parse
import subprocess
import platform

API_URL = "https://thinkprompt-api-v2.azurewebsites.net/api/v1"
RESULT = {"status": "pending", "token": None, "error": None}

def open_browser(url):
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["open", url], check=True)
        elif system == "Linux":
            subprocess.run(["xdg-open", url], check=True)
        elif system == "Windows":
            subprocess.run(["start", url], shell=True, check=True)
    except:
        print(f"Bitte oeffne manuell: {url}")

def device_authorize(redirect_uri):
    req = urllib.request.Request(
        f"{API_URL}/auth/device",
        data=json.dumps({"redirectUri": redirect_uri}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global RESULT
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

    # Create server first to reserve port
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", 0), CallbackHandler)
    port = httpd.server_address[1]
    redirect_uri = f"http://localhost:{port}/callback"

    # Initiate device auth with redirect URI
    try:
        auth = device_authorize(redirect_uri)
    except urllib.error.HTTPError as e:
        print(f"ERROR=api_error_{e.code}")
        print("STATUS=error")
        httpd.server_close()
        return
    except urllib.error.URLError:
        print("ERROR=network_error")
        print("STATUS=error")
        httpd.server_close()
        return
    except json.JSONDecodeError:
        print("ERROR=invalid_json")
        print("STATUS=error")
        httpd.server_close()
        return

    user_code = auth.get("userCode")
    verification_uri = auth.get("verificationUri", "https://thinkprompt.ai/device")

    if not user_code:
        print("ERROR=invalid_response")
        print("STATUS=error")
        httpd.server_close()
        return

    print(f"CODE={user_code}")
    print(f"Bitte gib diesen Code im Browser ein: {user_code}")

    # Open browser (server already listening)
    open_browser(verification_uri)

    # Wait for callback
    print("Warte auf Browser-Callback...")
    httpd.socket.settimeout(300)  # 5 min timeout
    try:
        httpd.handle_request()
    except socket.timeout:
        RESULT = {"status": "error", "error": "timeout"}
    except Exception as e:
        RESULT = {"status": "error", "error": f"server_error"}
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
DEVICEAUTH
```

Parse the output:
- Look for `CODE=XXXX-XXXX` - tell the user this code
- Look for `TOKEN=...` and `STATUS=complete` - extract the API key for Step 5
- If `STATUS=error`, show the error and abort

## Step 5: Save API Key

Once you have the `apiKey`, save it to `~/.claude/settings.json`:

1. Read current settings (or start with `{}` if file doesn't exist)
2. Merge the following, preserving existing configuration:

```json
{
  "env": {
    "THINKPROMPT_API_URL": "https://thinkprompt-api-v2.azurewebsites.net/api/v1",
    "THINKPROMPT_API_KEY": "<apiKey-from-callback>"
  }
}
```

3. Write the updated JSON back with proper formatting (2-space indentation)

## Step 6: Confirmation

Tell the user:
```
**Setup erfolgreich abgeschlossen!**

Dein ThinkPrompt Account wurde verknüpft und der API-Key wurde in `~/.claude/settings.json` gespeichert.

**Wichtig:** Bitte starte Claude Code neu, damit die Änderungen wirksam werden.

Nach dem Neustart kannst du alle ThinkPrompt-Features nutzen:
- `/feature-dev-tp` - Feature Development mit Style Guides
- `/quality-analysis` - Code Quality Analyse
- Und alle MCP-Tools (mcp__thinkprompt__*)

**Nächster Schritt:** Nach dem Neustart führe `/thinkprompt:setup-workspace` aus, um:
- Dein Projekt in ThinkPrompt anzulegen
- Style Guides basierend auf deiner Codebase zu erstellen
- Nützliche Prompts (Code Review, Feature Planning, etc.) zu generieren
```

## Error Handling

- **Network errors**: "Verbindung zu ThinkPrompt fehlgeschlagen. Bitte überprüfe deine Internetverbindung."
- **Invalid response**: "Unerwartete Antwort vom Server. Bitte versuche es später erneut."
- **Timeout (5 min)**: "Die Autorisierung hat zu lange gedauert. Bitte führe `/setup-thinkprompt` erneut aus."
- **File write errors**: Show the error and suggest manual configuration of `~/.claude/settings.json`

## Implementation Notes

- The Python script handles everything: callback server, device auth, and browser
- Uses local HTTP callback server for instant token delivery (no polling)
- The device code should be treated as sensitive (don't display it to the user)
- The user code is designed to be easily readable (no ambiguous characters like 0/O, 1/I/L)

### How the Script Works

1. Creates TCP server on port 0 (OS assigns free port)
2. Calls `/auth/device` with `redirectUri`
3. Validates response (userCode must exist)
4. Opens the browser with verification URL
5. Waits for callback (5 min timeout)
6. Browser redirects to localhost after user authenticates
7. Server receives token and outputs `TOKEN=...` and `STATUS=complete`
