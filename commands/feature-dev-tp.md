---
description: Feature development with automatic Style Guide loading from ThinkPrompt
argument-hint: [TASK-ID] <feature-description>
---

# Feature Development with ThinkPrompt Style Guides

You are implementing a feature using the feature-dev workflow, enhanced with automatic style guide loading from ThinkPrompt.

## WICHTIG: Planning Mode aktivieren

**ERSTE AKTION:** Verwende das `EnterPlanMode` Tool um in den Planning Mode zu wechseln. Dies ermöglicht eine gründliche Analyse und Planung bevor Code geschrieben wird.

Nach dem Wechsel in den Planning Mode, führe die folgenden Phasen durch:

---

## Pre-Phase 0: ThinkPrompt Task laden (Optional)

**Task-ID automatisch aus Beschreibung extrahieren:**

1. **Suche nach Task-ID Pattern** in `$ARGUMENTS`:
   - Pattern wie `ABC-123`, `PROJ-456`, oder reine Zahlen
   - Regex: `\b([A-Z]+-\d+|\d+)\b` (Word Boundary - findet Task-ID überall im Text)

2. **Wenn Task-ID gefunden:**
   - Task laden mit `mcp__plugin_thinkprompt_thinkprompt__get_task` (id: extrahierte Task-ID)
   - Task-ID für spätere Status-Updates speichern
   - Feature-ID merken falls vorhanden (`task.featureId`)
   - Projekt-ID merken (`task.projectId`)

3. **Task-Typ identifizieren:**
   - Prüfe `task.title`, `task.description`, `task.content` auf Keywords:
     - **Frontend-Task:** "frontend", "ui", "component", "page", "form", "button", "modal", "dialog", "style", "css", "tailwind", "react", "angular", "vue"
     - **Backend-Task:** "backend", "api", "endpoint", "service", "database", "migration", "dto", "controller", "resolver", "graphql"
   - Speichere Task-Typ für Phase 8

4. **Output:**
   ```
   📋 ThinkPrompt Task geladen: [task.title]
   Typ: [Frontend/Backend/Unbekannt]
   Status: [task.status]
   ```

**Wenn keine Task-ID gefunden:** Fahre ohne Task-Kontext fort.

**Fehlerbehandlung:**
- Wenn der Task nicht existiert (404): Output "⚠️ Task [ID] nicht gefunden. Fahre ohne Task-Kontext fort."
- Wenn API-Fehler: Output "⚠️ ThinkPrompt API nicht erreichbar. Fahre ohne Task-Kontext fort."
- In beiden Fällen: Phase 8 (ThinkPrompt Abschluss) überspringen

**Beispiel:** `/feature-dev-tp ABC-123 implementiere Login-Form` → extrahiert "ABC-123"

---

## Pre-Phase 1: Style Guide Loading

**CRITICAL: Before starting any feature development, you MUST attempt to load the appropriate style guide.**

### Step 1: Load Available Style Guides

Use `mcp__plugin_thinkprompt_thinkprompt__list_templates` with `type: "style"` to get all available style guide templates.
Store the list of templates with their `id`, `title`, `category`, `description`, and `useCaseHints`.

### Step 2: Detect Project Characteristics

Analyze the current project by checking for framework-specific indicators:

**JavaScript/TypeScript Projects (if `package.json` exists):**

1. Read `package.json` and extract `dependencies` and `devDependencies`
2. Use Glob to check for framework-specific config files:
   - `next.config.*` → Next.js
   - `nest-cli.json` → NestJS
   - `angular.json` → Angular
   - `vite.config.*` → Vite
   - `nuxt.config.*` → Nuxt
   - `svelte.config.*` → SvelteKit
   - `remix.config.*` → Remix
   - `astro.config.*` → Astro
   - `expo.json` or `app.json` with expo → React Native/Expo

3. Check for key dependencies:
   - `next` → Next.js
   - `@nestjs/core` → NestJS
   - `@angular/core` → Angular
   - `vue` → Vue.js
   - `svelte` → Svelte
   - `react` → React

**Python Projects (if `requirements.txt`, `pyproject.toml`, or `setup.py` exists):**
- Check for Django, FastAPI, Flask in dependencies

**Other Languages:**
- `Cargo.toml` → Rust
- `go.mod` → Go
- `pom.xml` or `build.gradle` → Java/Kotlin
- `composer.json` → PHP
- `Gemfile` → Ruby

**Result:** Create a list of detected characteristics (e.g., `["nextjs", "typescript", "react", "tailwind"]`)

### Step 3: Match Templates to Project

For each available style guide template from Step 1:
1. Check if `template.category` matches any detected characteristic (case-insensitive)
2. Check if `template.title` contains a detected framework name
3. Check if `template.description` mentions detected technologies
4. Check if any `useCaseHints` are relevant to the project

Create a list of matching templates, prioritizing:
- Exact category matches
- Title/description matches with framework names

### Step 4: Select Style Guide

**No matches found:**
- Output: "No matching style guide found. Proceeding with generic best practices."
- Continue without loading a template

**Exactly one match:**
- Automatically load the template using `mcp__plugin_thinkprompt_thinkprompt__get_template` with the template's `id`
- Output: "📚 Loaded Style Guide: [Template Title]"

**Multiple matches:**
- Use the `AskUserQuestion` tool to let the user choose:
  - Question: "Mehrere Style Guides passen zu deinem Projekt. Welchen möchtest du verwenden?"
  - Header: "Style Guide"
  - Options: List each matching template with its title as label and description
  - Add a final option: "Keinen verwenden" / "None"
- Load the selected template using `mcp__plugin_thinkprompt_thinkprompt__get_template`, or skip if user chose "None"

### Step 5: Acknowledge Style Guide

After loading (if a template was selected), output:
```
📚 Loaded Style Guide: [Template Title]
Category: [template.category]
```

Keep the style guide content in context for ALL subsequent phases.

---

## Feature Development Workflow (8 Phases)

Now proceed with the standard feature-dev workflow, applying the loaded style guide conventions throughout.

### Phase 1: Verstehen & Klärung

1. **Read and understand** the feature request: `$ARGUMENTS`
2. **Ask clarifying questions** if requirements are ambiguous
3. **Identify scope boundaries** - what's in/out of scope
4. **Check for dependencies** on other features or systems

### Phase 2: Codebase Exploration

1. **Explore relevant parts** of the codebase using the Task tool with `subagent_type=Explore`
2. **Identify existing patterns** that should be followed (per the style guide)
3. **Find related code** that the new feature will interact with
4. **Note architectural decisions** already made in the project

### Phase 3: Architektur Design

1. **Design the feature architecture** following the style guide patterns
2. **Identify files to create/modify**
3. **Define data structures** (types, interfaces, DTOs)
4. **Plan component hierarchy** (for frontend) or module structure (for backend)
5. **Consider edge cases** and error handling

### Phase 4: Implementierungsplanung

1. **Break down into small, testable tasks**
2. **Use TaskCreate** to track all implementation tasks
3. **Order tasks** by dependencies
4. **Identify potential blockers**

**NACH PHASE 4:** Verwende `ExitPlanMode` um den Plan dem User zur Genehmigung vorzulegen. Erst nach Genehmigung mit Phase 5 fortfahren.

---

### Phase 5: Implementierung

**Wenn Task-ID bekannt:** Setze Task-Status auf "in_progress":
```
mcp__plugin_thinkprompt_thinkprompt__update_task_status
  id: [task-id]
  status: "in_progress"
```

1. **Implement one task at a time**
2. **Follow the style guide** for:
   - File organization
   - Naming conventions
   - Code patterns (hooks, stores, services, DTOs, etc.)
   - Import ordering
   - Error handling
3. **Mark tasks complete** mit `TaskUpdate` (status: "completed") wenn fertig
4. **Test as you go** when possible

### Phase 6: Integration & Testing

#### 6.1 Verify Feature & Run Existing Tests

1. **Verify the feature works end-to-end**
2. **Check for TypeScript errors**: `pnpm typecheck` or `npm run lint`
3. **Run existing tests** to ensure no regressions

#### 6.2 Tests erstellen

1. **Identifiziere das Test-Framework** des Projekts:
   - JavaScript/TypeScript: Jest, Vitest, Mocha, Playwright Test
   - Python: pytest, unittest
   - Andere: Framework-spezifisch

2. **Erstelle Tests für die neue Funktionalität:**

   **Unit Tests:**
   - Teste einzelne Funktionen/Methoden isoliert
   - Mocke externe Dependencies
   - Teste Edge Cases und Error Handling

   **Integration Tests:**
   - Teste API-Endpoints (Request/Response)
   - Teste Datenbank-Interaktionen
   - Teste Service-zu-Service Kommunikation

   **Component Tests (Frontend):**
   - Teste Komponenten-Rendering
   - Teste User-Interaktionen (Clicks, Input)
   - Teste State-Changes

3. **Führe alle Tests aus** und stelle sicher, dass sie bestehen:
   ```bash
   # Beispiele je nach Framework
   pnpm test
   npm run test
   pytest
   ```

#### 6.3 Frontend Browser-Tests mit Playwright (nur bei Frontend-Tasks)

**Voraussetzung:** Playwright MCP Server muss konfiguriert sein.
Falls nicht verfügbar: Überspringe Browser-Tests und notiere "⚠️ Playwright nicht konfiguriert - E2E Tests übersprungen"

**Wenn das Feature UI-Komponenten beinhaltet:**

1. **Starte die Anwendung lokal** (falls nicht bereits laufend):
   ```bash
   pnpm dev
   # oder npm run dev
   ```

2. **Verwende Playwright MCP Tools für E2E-Tests:**

   ```
   # Navigiere zur relevanten Seite
   mcp__plugin_playwright_playwright__browser_navigate
     url: "http://localhost:3000/[feature-path]"

   # Hole Accessibility-Snapshot für Element-Referenzen
   mcp__plugin_playwright_playwright__browser_snapshot

   # Interagiere mit Elementen (verwende ref aus Snapshot)
   mcp__plugin_playwright_playwright__browser_click
     element: "Submit button"
     ref: "[ref-from-snapshot]"

   mcp__plugin_playwright_playwright__browser_type
     element: "Email input"
     ref: "[ref-from-snapshot]"
     text: "test@example.com"

   mcp__plugin_playwright_playwright__browser_fill_form
     fields: [{"selector": "#email", "value": "test@example.com"}]

   # Warte auf Ergebnis
   mcp__plugin_playwright_playwright__browser_wait_for
     text: "Success"
     timeout: 5000

   # Erstelle Screenshot als visuellen Beweis
   mcp__plugin_playwright_playwright__browser_take_screenshot
     filename: "feature-test-result.png"
   ```

3. **Teste mindestens:**
   - ✅ **Happy Path:** Normale Nutzung des Features funktioniert
   - ⚠️ **Error Case:** Fehlerbehandlung funktioniert (z.B. leeres Formular, ungültige Eingabe)

4. **Output:**
   ```
   🎭 Playwright Tests abgeschlossen:
   - Happy Path: ✅
   - Error Handling: ✅
   - Screenshots: feature-test-result.png
   ```

### Phase 7: Review & Feinschliff

#### 7.1 Automatischer Code Review

**Verwende den `thinkprompt:code-reviewer` Subagent für einen umfassenden Code Review.**

> **Hinweis:** Dies ist ein Claude Code Subagent (nicht ein MCP Tool). Er wird über das Task tool mit `subagent_type` aufgerufen.

```
Task tool:
  subagent_type: "thinkprompt:code-reviewer"
  prompt: "Review the implemented feature for architecture, code quality, and security"
```

Der Agent:
- Lädt automatisch den passenden Style Guide (basierend auf Projekt-Typ)
- Prüft Architektur und Code-Struktur
- Identifiziert Sicherheitsprobleme
- Bewertet Code-Qualität und Wartbarkeit
- Gibt priorisierte Verbesserungsvorschläge

**Output:**
```
🔍 Code Review abgeschlossen
- Style Guide Compliance: [✅/⚠️]
- Architektur: [Bewertung]
- Sicherheit: [Bewertung]
- Code-Qualität: [Bewertung]
- Empfehlungen: [Liste]
```

**Fehlerbehandlung:**
- Wenn Agent nicht verfügbar: Führe manuellen Code Review durch (siehe 7.2)
- Wenn kein Style Guide in Pre-Phase 1 geladen: Agent verwendet generische Best Practices

#### 7.2 Manuelle Nacharbeit

Nach dem automatischen Review:
1. **Behebe kritische Issues** aus dem Review
2. **Clean up any TODO comments**
3. **Ensure consistent formatting**
4. **Remove debug code**
5. **Summarize what was implemented**

### Phase 8: ThinkPrompt Abschluss

**Diese Phase nur ausführen, wenn in Pre-Phase 0 eine Task-ID geladen wurde.**

#### 8.1 Task auf Review setzen

Setze den Task-Status auf "review":

```
mcp__plugin_thinkprompt_thinkprompt__update_task_status
  id: [gespeicherte-task-id]
  status: "review"
```

**Output:** `✅ Task "[task.title]" auf **Review** gesetzt`

#### 8.2 Frontend-Folgetask erstellen (bei Backend-Tasks)

**Nur wenn BEIDE Bedingungen erfüllt sind:**
1. Der implementierte Task war ein **Backend-Task** (erkannt in Pre-Phase 0)
2. Die Implementierung hat **neue API-Endpoints erstellt** oder **bestehende Datenstrukturen geändert**, die im Frontend konsumiert werden

**Ablauf:**

1. **Frage den User:**
   ```
   AskUserQuestion:
     question: "Die Backend-Implementierung ist abgeschlossen. Soll ein Frontend-Task für die UI-Integration erstellt werden?"
     header: "Frontend-Task"
     options:
       - label: "Ja, Task erstellen"
         description: "Erstellt einen neuen Task mit API-Dokumentation und Integrations-Hinweisen"
       - label: "Nein, nicht nötig"
         description: "Kein Frontend-Task erforderlich"
   ```

2. **Bei "Ja":** Erstelle den Frontend-Task:

   ```
   mcp__plugin_thinkprompt_thinkprompt__create_task
     projectId: [projekt-id-vom-original-task]
     featureId: [feature-id-falls-vorhanden]
     title: "Frontend: [Feature-Name] UI Integration"
     description: "UI-Integration für das Backend-Feature [Feature-Name]"
     priority: [gleiche-priority-wie-original]
     content: |
       ## Übersicht
       Frontend-Integration für das implementierte Backend-Feature.

       ## API Endpoints

       ### [Endpoint-Name]
       - **URL:** `[METHOD] /api/[path]`
       - **Request Body:**
         ```typescript
         interface RequestDTO {
           // ...
         }
         ```
       - **Response:**
         ```typescript
         interface ResponseDTO {
           // ...
         }
         ```

       ## Beispiel API-Call

       ```typescript
       const response = await fetch('/api/[path]', {
         method: '[METHOD]',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(data)
       });
       ```

       ## Integrations-Hinweise
       - [Hinweise zur UI-Integration]
       - [Erforderliche Komponenten]
       - [State Management Überlegungen]
   ```

3. **Füge Kommentar zum Original-Task hinzu:**

   ```
   mcp__plugin_thinkprompt_thinkprompt__add_task_comment
     taskId: [original-task-id]
     content: "✅ Backend-Implementierung abgeschlossen. Frontend-Task erstellt: [neuer-task-titel]"
   ```

4. **Output:**
   ```
   📋 Frontend-Task erstellt: "[neuer-task-titel]"
   🔗 Kommentar zum Original-Task hinzugefügt
   ```

#### 8.3 Abschluss-Zusammenfassung

```
## ✅ Feature-Entwicklung abgeschlossen

**Feature:** [feature-beschreibung]

**Implementiert:**
- [Liste der erstellten/geänderten Dateien]

**Tests:**
- [X] Unit Tests erstellt
- [X] Integration Tests (falls zutreffend)
- [X] Playwright E2E Tests (falls Frontend)

**ThinkPrompt:**
- [X] Task auf Review gesetzt
- [Optional] Frontend-Folgetask erstellt
```

---

## Style Guide Application Checklist

Apply the conventions from the loaded style guide throughout all phases. General checks:

- [ ] Following the file/folder organization from the style guide
- [ ] Using the naming conventions specified
- [ ] Applying recommended code patterns
- [ ] Following import ordering conventions
- [ ] Implementing proper error handling as per style guide
- [ ] Using TypeScript/type annotations as recommended
- [ ] Following component/module structure patterns

---

## Feature Request

**Implementing:** `$ARGUMENTS`

Begin with Pre-Phase 0 (ThinkPrompt Task laden), then Pre-Phase 1 (Style Guide Loading), and proceed through all 8 phases systematically.

---

## Verfügbare MCP Tools Referenz

### ThinkPrompt Tools

| Tool | Beschreibung |
|------|-------------|
| `mcp__plugin_thinkprompt_thinkprompt__get_task` | Task laden (id) |
| `mcp__plugin_thinkprompt_thinkprompt__update_task_status` | Status setzen (id, status: open/in_progress/blocked/review/done) |
| `mcp__plugin_thinkprompt_thinkprompt__create_task` | Neuen Task erstellen (projectId, title, description, content, priority, featureId) |
| `mcp__plugin_thinkprompt_thinkprompt__add_task_comment` | Kommentar hinzufügen (taskId, content) |
| `mcp__plugin_thinkprompt_thinkprompt__list_templates` | Style Guide Templates auflisten (type: "style") |
| `mcp__plugin_thinkprompt_thinkprompt__get_template` | Template laden (id) |

### Playwright Tools (für Frontend-Tests)

| Tool | Beschreibung |
|------|-------------|
| `mcp__plugin_playwright_playwright__browser_navigate` | URL öffnen |
| `mcp__plugin_playwright_playwright__browser_snapshot` | Accessibility-Snapshot (Element-Refs) |
| `mcp__plugin_playwright_playwright__browser_click` | Element klicken |
| `mcp__plugin_playwright_playwright__browser_type` | Text eingeben |
| `mcp__plugin_playwright_playwright__browser_fill_form` | Formular ausfüllen |
| `mcp__plugin_playwright_playwright__browser_take_screenshot` | Screenshot erstellen |
| `mcp__plugin_playwright_playwright__browser_wait_for` | Auf Element/Text warten |
