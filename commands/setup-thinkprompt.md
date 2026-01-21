---
description: Configure ThinkPrompt API credentials for this plugin
---

# ThinkPrompt Plugin Setup

You are helping the user configure their ThinkPrompt API credentials.

## Step 1: Welcome & Information

Tell the user:
"**ThinkPrompt Plugin Setup**

Um das ThinkPrompt Plugin zu nutzen, benötigst du einen API-Key.

Du kannst deinen API-Key hier erstellen: https://thinkprompt.app/settings/api-keys"

## Step 2: Ask for API Key

Use the `AskUserQuestion` tool to ask for the API key:
- Question: "Bitte gib deinen ThinkPrompt API-Key ein:"
- Header: "API Key"
- Options: Provide a text input option (user will select "Other" to enter their key)

## Step 3: Read Current Settings

Read the file `~/.claude/settings.json`. If it doesn't exist or is empty, start with an empty JSON object `{}`.

## Step 4: Update Settings

Merge the following into the settings JSON, preserving any existing configuration:

```json
{
  "env": {
    "THINKPROMPT_API_URL": "https://api.thinkprompt.ai/api/v1",
    "THINKPROMPT_API_KEY": "<the-key-from-step-2>"
  }
}
```

If there's already an `env` object, add/update only these two keys without removing other environment variables.

## Step 5: Write Updated Settings

Write the updated JSON back to `~/.claude/settings.json` with proper formatting (2-space indentation).

## Step 6: Confirmation

Tell the user:
"**Setup abgeschlossen!**

Dein ThinkPrompt API-Key wurde in `~/.claude/settings.json` gespeichert.

**Wichtig:** Bitte starte Claude Code neu, damit die Änderungen wirksam werden.

Nach dem Neustart kannst du alle ThinkPrompt-Features nutzen:
- `/feature-dev-tp` - Feature Development mit Style Guides
- `/quality-analysis` - Code Quality Analyse
- Und alle MCP-Tools (mcp__thinkprompt__*)"

## Error Handling

- If the user cancels or provides an empty key, inform them that the setup was cancelled and they can run `/setup-thinkprompt` again later.
- If there's an error reading/writing the settings file, explain the error and suggest manual configuration.
