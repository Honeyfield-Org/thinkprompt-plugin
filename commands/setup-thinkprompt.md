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

## Step 2: Run Device Authorization

Run the device authorization script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/device-auth.py"
```

The script outputs key=value pairs. Parse them:
- `USER_CODE=XXXX-XXXX` - The code the user needs to confirm
- `VERIFY_URL=...` - The URL that was opened
- `BROWSER=opened` - Browser was opened
- `TOKEN=...` - The API key (on success)
- `STATUS=complete` or `STATUS=error`
- `ERROR=...` - Error message (on failure)

**IMPORTANT:** As soon as you see `USER_CODE=...` in the output, tell the user:

"**Dein Login-Code: {USER_CODE}**

Der Browser wurde geöffnet. Bitte bestätige den Code dort.

Warte auf Bestätigung..."

Then wait for the script to complete (it waits for the callback).

## Step 3: Handle Result

**On SUCCESS** (`STATUS=complete`):

Save the token to `~/.claude/settings.json`:

1. Read current settings (or start with `{}` if file doesn't exist)
2. Merge the following, preserving existing configuration:

```json
{
  "env": {
    "THINKPROMPT_API_URL": "https://thinkprompt-api-v2.azurewebsites.net/api/v1",
    "THINKPROMPT_API_KEY": "<TOKEN-from-script>"
  }
}
```

3. Write the updated JSON back with proper formatting (2-space indentation)

Then tell the user:
```
**Setup erfolgreich abgeschlossen!**

Dein ThinkPrompt Account wurde verknüpft und der API-Key wurde gespeichert.

**Wichtig:** Bitte starte Claude Code neu, damit die Änderungen wirksam werden.

Nach dem Neustart kannst du:
- `/setup-workspace` - Projekt einrichten mit Style Guides
- `/feature-dev-tp` - Feature Development
- `/quality-analysis` - Code Quality Analyse
```

**On ERROR** (`STATUS=error`):

Tell the user the error and suggest:
- Check internet connection
- Try `/setup-thinkprompt` again
- Or manually get API key from https://thinkprompt.app/settings

## Error Handling

- **Network errors**: "Verbindung zu ThinkPrompt fehlgeschlagen. Bitte überprüfe deine Internetverbindung."
- **Timeout (5 min)**: "Die Autorisierung hat zu lange gedauert. Bitte führe `/setup-thinkprompt` erneut aus."
- **File write errors**: Show the error and suggest manual configuration of `~/.claude/settings.json`
