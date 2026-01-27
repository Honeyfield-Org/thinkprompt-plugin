---
description: Browse and apply ThinkPrompt templates (Style Guides and Example Prompts)
argument-hint: "[styles|examples|template-name]"
---

# ThinkPrompt Template Management

Du hilfst dem User beim Browsen und Anwenden von Templates in ThinkPrompt.

Templates gibt es in zwei Typen:
- **Style Guides** (`type: "style"`) - Code-Konventionen und Best Practices
- **Example Prompts** (`type: "example"`) - Beispiel-Prompts als Inspiration

---

## Phase 1: Argument verarbeiten

Prüfe `$ARGUMENTS`:

### Fall A: Kein Argument
→ Zeige alle Templates (Phase 2)

### Fall B: "styles" oder "style"
→ Zeige nur Style Guides (Phase 2 mit Filter)

### Fall C: "examples" oder "example"
→ Zeige nur Example Prompts (Phase 2 mit Filter)

### Fall D: "new" oder "neu"
→ Neues Template erstellen (Phase 5)

### Fall E: Suchbegriff
→ Suche Templates (Phase 3)

---

## Phase 2: Template-Übersicht

### Schritt 2.1: Templates laden

Verwende `mcp__thinkprompt__list_templates` mit:
- `type`: "style" oder "example" (falls Filter)
- `limit`: 20

### Schritt 2.2: Übersicht formatieren

```
📚 **Templates**

## Style Guides

| # | Titel | Kategorie | Sprache |
|---|-------|-----------|---------|
| 1 | Next.js Style Guide | nextjs | de |
| 2 | NestJS Best Practices | nestjs | en |
| 3 | React Patterns | react | de |

## Example Prompts

| # | Titel | Kategorie | Beschreibung |
|---|-------|-----------|--------------|
| 1 | PR Review Template | code-review | Strukturiertes PR Review |
| 2 | API Design Prompt | api | REST API Design Patterns |

---
Gesamt: X Style Guides, Y Example Prompts

💡 `/templates styles` nur Style Guides | `/templates nextjs` zum Anzeigen
```

### Schritt 2.3: Template auswählen

Verwende `AskUserQuestion`:
- Question: "Möchtest du ein Template anzeigen?"
- Header: "Template"
- Options: Top 4 Templates + "Keines"

Falls User eines wählt → Phase 4 (Anzeigen/Anwenden)

---

## Phase 3: Template suchen

### Schritt 3.1: Suchen

Verwende `mcp__thinkprompt__list_templates` mit:
- `search`: Der Suchbegriff aus `$ARGUMENTS`

Zusätzlich nach Kategorie filtern falls Suchbegriff ein bekanntes Framework ist:
- nextjs, nestjs, angular, vue, react, svelte, python, rust, go

### Schritt 3.2: Ergebnisse zeigen

**Keine Treffer:**
```
🔍 Keine Templates für "[Suchbegriff]" gefunden.

💡 `/templates` für alle Templates | `/templates new` zum Erstellen
```

**Ein Treffer:**
→ Direkt zu Phase 4 (Anzeigen)

**Mehrere Treffer:**
Zeige Liste und frage welches angezeigt werden soll.

---

## Phase 4: Template anzeigen/anwenden

### Schritt 4.1: Template laden

Verwende `mcp__thinkprompt__get_template` mit der `id`.

### Schritt 4.2: Template anzeigen

**Für Style Guides:**
```
📚 **[Titel]**

**Typ:** Style Guide
**Kategorie:** [category]
**Sprache:** [language]

---

[Template Content - der eigentliche Style Guide]

---

**Use Case Hints:**
- [hint 1]
- [hint 2]
```

**Für Example Prompts:**
```
📝 **[Titel]**

**Typ:** Example Prompt
**Kategorie:** [category]

---

[Template Content - der Beispiel-Prompt]

---

**Wann nutzen:**
- [hint 1]
- [hint 2]
```

### Schritt 4.3: Aktionen anbieten

**Für Style Guides:**
Verwende `AskUserQuestion`:
- Question: "Was möchtest du mit diesem Style Guide tun?"
- Header: "Aktion"
- Options:
  1. "Für Projekt merken" - Als aktiven Style Guide setzen
  2. "In Prompt umwandeln" - Als Prompt-Kontext erstellen
  3. "Kopieren" - Zum Einfügen
  4. "Nichts"

**Für Example Prompts:**
Verwende `AskUserQuestion`:
- Question: "Was möchtest du mit diesem Example Prompt tun?"
- Header: "Aktion"
- Options:
  1. "Als Prompt erstellen" - Neuen Prompt basierend darauf
  2. "Kopieren" - Zum Einfügen
  3. "Nichts"

### Schritt 4.4: Aktionen ausführen

**"Als Prompt erstellen":**
Verwende `mcp__thinkprompt__create_prompt` mit:
- `title`: "[Template Title]" (User kann anpassen)
- `content`: Template content
- Variablen automatisch aus `{{var}}` extrahieren

Output: "✅ Prompt **[Titel]** erstellt! Nutze `/prompts [titel]` zum Ausführen."

**"Für Projekt merken":**
Informiere den User:
```
📚 Style Guide **[Titel]** gemerkt.

Der `code-reviewer` Agent und `/feature-dev-tp` werden diesen Style Guide
automatisch laden wenn sie zum Projekt passen.

Kategorie: [category]
```

---

## Phase 5: Neues Template erstellen

### Schritt 5.1: Typ wählen

Verwende `AskUserQuestion`:
- Question: "Welchen Template-Typ möchtest du erstellen?"
- Header: "Typ"
- Options:
  1. "Style Guide" - Code-Konventionen für ein Framework/Projekt
  2. "Example Prompt" - Beispiel-Prompt als Inspiration

### Schritt 5.2: Grunddaten abfragen

**Titel:**
- Question: "Wie soll das Template heißen?"
- Header: "Titel"

**Kategorie:**
- Question: "Für welches Framework/Thema ist das Template?"
- Header: "Kategorie"
- Options:
  1. "nextjs"
  2. "nestjs"
  3. "angular"
  4. "react"
  + "Other" für eigene

**Sprache:**
- Question: "In welcher Sprache ist das Template?"
- Header: "Sprache"
- Options:
  1. "de - Deutsch"
  2. "en - English"

### Schritt 5.3: Content erstellen

**Für Style Guides:**
Biete an, den Style Guide automatisch zu generieren:

Verwende `AskUserQuestion`:
- Question: "Wie möchtest du den Style Guide erstellen?"
- Header: "Methode"
- Options:
  1. "Aus Code generieren" - Analysiert aktuelle Codebase
  2. "Manuell schreiben" - Eigenen Content eingeben
  3. "Template verwenden" - Standard-Struktur nutzen

**"Aus Code generieren":**
Analysiere die Codebase wie in `/setup-workspace` beschrieben und generiere den Style Guide.

**"Template verwenden":**
```markdown
# [Framework] Style Guide

## Projektstruktur

```
src/
├── components/    # React-Komponenten
├── hooks/         # Custom Hooks
├── utils/         # Utility-Funktionen
└── types/         # TypeScript Types
```

## Namenskonventionen

### Dateien
- Komponenten: `PascalCase.tsx`
- Hooks: `useCamelCase.ts`
- Utils: `camelCase.ts`

### Code
- Funktionen: `camelCase`
- Konstanten: `UPPER_SNAKE_CASE`
- Types/Interfaces: `PascalCase`

## Import-Reihenfolge

1. React/Framework imports
2. External packages
3. Internal modules (@/)
4. Relative imports
5. Types
6. Styles

## Code-Patterns

### Komponenten
- Functional Components mit TypeScript
- Props als Interface definieren
- Destructuring in Parametern

### Error Handling
- try/catch für async Operationen
- Error Boundaries für UI-Fehler

## Testing

- Test-Dateien neben Source: `Component.test.tsx`
- Describe/it Pattern
- React Testing Library
```

**Für Example Prompts:**
User gibt den Prompt-Text ein.

### Schritt 5.4: Use Case Hints

Verwende `AskUserQuestion` mit `multiSelect: true`:
- Question: "Wann sollte dieses Template verwendet werden?"
- Header: "Use Cases"
- Options:
  1. "Code Review"
  2. "Neue Features"
  3. "Bug Fixes"
  4. "Refactoring"
  + "Other" für eigene

### Schritt 5.5: Template erstellen

Verwende `mcp__thinkprompt__create_template` mit:
- `title`: Eingegebener Titel
- `type`: "style" oder "example"
- `category`: Gewählte Kategorie
- `language`: Gewählte Sprache
- `content`: Erstellter Content
- `useCaseHints`: Gewählte Hints

### Schritt 5.6: Bestätigung

```
✅ **Template erstellt!**

📚 **[Titel]**
Typ: [Style Guide / Example Prompt]
Kategorie: [category]

💡 Das Template ist jetzt für alle ThinkPrompt-Features verfügbar.
```

---

## Schnellbefehle

| Befehl | Beschreibung |
|--------|--------------|
| `/templates` | Alle Templates anzeigen |
| `/templates styles` | Nur Style Guides |
| `/templates examples` | Nur Example Prompts |
| `/templates nextjs` | Nach Framework suchen |
| `/templates new` | Neues Template erstellen |

---

## Error Handling

### Keine Templates vorhanden
```
📚 Noch keine Templates vorhanden.

💡 Nutze `/templates new` um dein erstes Template zu erstellen,
   oder `/setup-workspace` um Standard-Templates anzulegen.
```

### API-Fehler
"⚠️ ThinkPrompt API nicht erreichbar. Prüfe ob `/setup-thinkprompt` ausgeführt wurde."
