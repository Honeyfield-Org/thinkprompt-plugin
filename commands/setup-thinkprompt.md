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

## Step 2: Get Device Code

First, find a free port and request a device code:

```bash
# Find free port
PORT=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")

# Get API URL (default to production)
API_URL="${THINKPROMPT_API_URL:-https://thinkprompt-api-v2.azurewebsites.net/api/v1}"

# Request device code
curl -s -X POST "${API_URL}/auth/device" \
  -H "Content-Type: application/json" \
  -d "{\"redirectUri\": \"http://localhost:${PORT}/callback\"}"
```

Parse the JSON response and extract:
- `data.userCode` - the code to show the user
- `data.verificationUri` - the URL to open

**IMPORTANT:** Immediately show the user the code in a prominent way:

"**Dein Login-Code: {userCode}**

Bitte gib diesen Code im Browser ein."

## Step 3: Open Browser with Code

Determine the verification URL:
- If `THINKPROMPT_API_URL` contains "localhost", use `http://localhost:3002/device`
- Otherwise use the `verificationUri` from the response

Append the user code as query parameter so it's pre-filled:

```bash
open "{verification_url}?code={userCode}"
```

Tell the user: "Browser wurde geöffnet. Bitte bestätige den Code dort."

## Step 4: Wait for Callback

Start the callback server to receive the token:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/device-auth-callback.py" {PORT}
```

Parse the output:
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

- Two-step process: curl gets the code (instant output), then Python waits for callback
- The callback script is at `${CLAUDE_PLUGIN_ROOT}/scripts/device-auth-callback.py`
- The user code MUST be shown immediately after curl returns, BEFORE opening the browser
- For local dev: if `THINKPROMPT_API_URL` contains "localhost", use `http://localhost:3002/device` as UI

### Flow

1. Find free port with Python one-liner
2. curl to `/auth/device` with `redirectUri` → get `userCode` immediately
3. **Show userCode to user** (this is the key UX improvement!)
4. Open browser with verification URL
5. Start callback server on the reserved port
6. Wait for redirect with token (5 min timeout)
7. Extract token from callback
