---
description: List, search, execute, and create ThinkPrompt prompts
argument-hint: "[search|new|prompt-name]"
---

# ThinkPrompt Prompt Management

Du hilfst dem User beim Verwalten und Ausführen von Prompts in ThinkPrompt.

---

## Phase 1: Argument verarbeiten

Prüfe `$ARGUMENTS`:

### Fall A: Kein Argument
→ Zeige Prompt-Übersicht (Phase 2)

### Fall B: "new" oder "neu"
→ Neuen Prompt erstellen (Phase 5)

### Fall C: Suchbegriff
→ Suche und ggf. ausführen (Phase 3)

---

## Phase 2: Prompt-Übersicht

### Schritt 2.1: Prompts laden

Verwende `mcp__thinkprompt__list_prompts` mit `limit: 20`.

### Schritt 2.2: Übersicht formatieren

```
📝 **Deine Prompts**

| # | Titel | Beschreibung | Variablen |
|---|-------|--------------|-----------|
| 1 | Code Review | Strukturiertes Review | 2 |
| 2 | Feature Planning | Feature-Breakdown | 3 |
| 3 | Bug Report | Bug-Analyse | 4 |
| 4 | Commit Message | Conventional Commits | 2 |

---
Gesamt: X Prompts

💡 `/prompts code review` zum Ausführen | `/prompts new` zum Erstellen
```

### Schritt 2.3: Quick-Execute anbieten

Verwende `AskUserQuestion`:
- Question: "Möchtest du einen Prompt ausführen?"
- Header: "Ausführen"
- Options: Top 4 Prompts als Optionen + "Keinen"

Falls User einen wählt → Phase 4 (Ausführen)

---

## Phase 3: Prompt suchen

### Schritt 3.1: Suchen

Verwende `mcp__thinkprompt__list_prompts` mit:
- `search`: Der Suchbegriff aus `$ARGUMENTS`

### Schritt 3.2: Ergebnisse zeigen

**Keine Treffer:**
```
🔍 Keine Prompts für "[Suchbegriff]" gefunden.

💡 `/prompts` für alle Prompts | `/prompts new` zum Erstellen
```

**Ein Treffer:**
→ Direkt zu Phase 4 (Ausführen)

**Mehrere Treffer:**
```
🔍 **Suchergebnisse für "[Suchbegriff]"**

| # | Titel | Beschreibung |
|---|-------|--------------|
| 1 | Code Review | Strukturiertes Review |
| 2 | Code Analysis | Tiefe Code-Analyse |
```

Dann `AskUserQuestion`:
- Question: "Welchen Prompt möchtest du ausführen?"
- Header: "Prompt"
- Options: Gefundene Prompts

---

## Phase 4: Prompt ausführen

### Schritt 4.1: Prompt-Details laden

Verwende `mcp__thinkprompt__get_prompt` mit der `id` des gewählten Prompts.

### Schritt 4.2: Prompt anzeigen

```
📝 **[Titel]**

[Beschreibung]

**Variablen:**
- `code` (textarea, required): Der zu überprüfende Code
- `context` (text, optional): Zusätzlicher Kontext
```

### Schritt 4.3: Variablen abfragen

Für jede Variable im Prompt:

**Für required Variablen:**
Verwende `AskUserQuestion`:
- Question: "[Variable Label]: [Variable Description]"
- Header: "[Variable Name]"
- Options für `select` Typ, sonst User gibt via "Other" ein

**Für optional Variablen:**
Frage ob der User einen Wert angeben möchte.

### Schritt 4.4: Prompt zusammenbauen

Ersetze alle `{{variable}}` Platzhalter im Prompt-Content mit den eingegebenen Werten.

### Schritt 4.5: Ausgabe

```
---

📋 **Prompt: [Titel]**

[Zusammengebauter Prompt-Content mit eingesetzten Variablen]

---

💡 Kopiere diesen Prompt oder nutze ihn direkt in deinem nächsten Request.
```

---

## Phase 5: Neuen Prompt erstellen

### Schritt 5.1: Grunddaten abfragen

**Titel:**
Verwende `AskUserQuestion`:
- Question: "Wie soll der Prompt heißen?"
- Header: "Titel"
- Options: (User gibt via "Other" ein)

**Beschreibung:**
Verwende `AskUserQuestion`:
- Question: "Kurze Beschreibung des Prompts (optional):"
- Header: "Beschreibung"
- Options: "Überspringen" + "Other" für Eingabe

### Schritt 5.2: Prompt-Typ wählen

Verwende `AskUserQuestion`:
- Question: "Welche Art von Prompt möchtest du erstellen?"
- Header: "Typ"
- Options:
  1. "Analyse" - Code Review, Bug-Analyse, Security Check
  2. "Generierung" - Code, Docs, Tests generieren
  3. "Planung" - Feature-Planning, Task-Breakdown
  4. "Frei" - Eigene Struktur

### Schritt 5.3: Template basierend auf Typ

**Analyse-Template:**
```markdown
Analysiere folgenden Code/Text:

```
{{input}}
```

**Kontext:** {{context}}

Prüfe auf:
1. [Aspekt 1]
2. [Aspekt 2]
3. [Aspekt 3]

Output-Format:
- Zusammenfassung
- Gefundene Issues (Severity/Location/Beschreibung)
- Empfehlungen
```

**Generierungs-Template:**
```markdown
Generiere {{output_type}} basierend auf:

**Anforderungen:**
{{requirements}}

**Kontext:**
{{context}}

Beachte:
- [Regel 1]
- [Regel 2]

Format: [Gewünschtes Format]
```

**Planungs-Template:**
```markdown
Plane die Umsetzung für:

**Ziel:** {{goal}}

**Anforderungen:**
{{requirements}}

**Constraints:**
{{constraints}}

Erstelle:
1. Task-Breakdown mit Abhängigkeiten
2. Risikoanalyse
3. Zeitschätzung (optional)
```

**Frei:**
Leerer Content, User schreibt selbst.

### Schritt 5.4: Content bearbeiten

Zeige das Template und frage:
- Question: "Möchtest du den Prompt-Inhalt anpassen?"
- Header: "Bearbeiten"
- Options:
  1. "Template verwenden" - So übernehmen
  2. "Anpassen" - User gibt neuen Content ein

### Schritt 5.5: Variablen definieren

Extrahiere automatisch alle `{{variable}}` aus dem Content.

Für jede Variable frage:
- Question: "Konfiguration für Variable `{{name}}`:"
- Header: "[name]"
- Options:
  1. "text - Kurze Eingabe"
  2. "textarea - Längerer Text"
  3. "select - Auswahl" (dann Optionen abfragen)
  4. "number - Zahl"

Frage auch ob required (ja/nein).

### Schritt 5.6: Prompt erstellen

Verwende `mcp__thinkprompt__create_prompt` mit:
- `title`: Eingegebener Titel
- `description`: Eingegebene Beschreibung
- `content`: Prompt-Content
- `variables`: Array der definierten Variablen

### Schritt 5.7: Bestätigung

```
✅ **Prompt erstellt!**

📝 **[Titel]**
[Beschreibung]

Variablen: [Liste der Variablen]

💡 Nutze `/prompts [titel]` zum Ausführen
```

---

## Schnellbefehle

| Befehl | Beschreibung |
|--------|--------------|
| `/prompts` | Alle Prompts anzeigen |
| `/prompts new` | Neuen Prompt erstellen |
| `/prompts code review` | Prompt suchen/ausführen |
| `/prompts bug` | Prompts mit "bug" suchen |

---

## Error Handling

### Keine Prompts vorhanden
```
📝 Du hast noch keine Prompts.

💡 Nutze `/prompts new` um deinen ersten Prompt zu erstellen,
   oder `/setup-workspace` um Standard-Prompts anzulegen.
```

### API-Fehler
"⚠️ ThinkPrompt API nicht erreichbar. Prüfe ob `/setup-thinkprompt` ausgeführt wurde."
