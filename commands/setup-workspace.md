---
description: Set up ThinkPrompt for your project. Analyzes codebase, creates project, style guides, and useful prompts.
---

# ThinkPrompt Workspace Setup

You are helping the user set up ThinkPrompt for their project. This involves analyzing the codebase, creating a project, setting up style guides, and creating useful prompts.

---

## Phase 1: Project Analysis

Analyze the current codebase to detect frameworks, languages, and tools.

### Step 1.1: Framework Detection

Use Glob to check for framework-specific config files:

```
next.config.* → Next.js
nest-cli.json → NestJS
angular.json → Angular
vite.config.* → Vite (check package.json for vue/react)
nuxt.config.* → Nuxt
svelte.config.* → SvelteKit
remix.config.* → Remix
astro.config.* → Astro
expo.json or app.json with expo → React Native/Expo
```

### Step 1.2: Read Package/Dependency Files

Check for and read dependency files:

**JavaScript/TypeScript (package.json):**
- Extract `dependencies` and `devDependencies`
- Check for: `next`, `@nestjs/core`, `@angular/core`, `vue`, `svelte`, `react`, `express`, `fastify`

**Python (requirements.txt, pyproject.toml, setup.py):**
- Check for: Django, FastAPI, Flask, SQLAlchemy

**Other Languages:**
- `Cargo.toml` → Rust
- `go.mod` → Go
- `pom.xml` or `build.gradle` → Java/Kotlin
- `composer.json` → PHP (Laravel, Symfony)
- `Gemfile` → Ruby (Rails)

### Step 1.3: Detect Additional Tools

Check for configuration files:
- `tsconfig.json` → TypeScript
- `jest.config.*` or `vitest.config.*` → Testing framework
- `tailwind.config.*` → Tailwind CSS
- `eslint.config.*` or `.eslintrc.*` → ESLint
- `prettier.config.*` or `.prettierrc*` → Prettier
- `docker-compose.yml` or `Dockerfile` → Docker

### Step 1.4: Output Summary

Create a summary of detected technologies. Output:

"🔍 **Erkannte Technologien:**
- **Framework:** [Main Framework]
- **Sprache:** [TypeScript/JavaScript/Python/etc.]
- **Testing:** [Jest/Vitest/Pytest/etc.]
- **Styling:** [Tailwind/SCSS/etc.]
- **Tools:** [ESLint, Prettier, Docker, etc.]"

Store the detected characteristics as a list (e.g., `["nextjs", "typescript", "react", "tailwind", "jest"]`) for later use.

---

## Phase 2: Create ThinkPrompt Project

### Step 2.1: Check Existing Projects

Use `mcp__thinkprompt__list_projects` to retrieve existing projects.

Check if a project with a similar name already exists.

### Step 2.2: Handle Existing Project

**If a project with similar name exists:**
Use `AskUserQuestion` to ask:
- Question: "Ein Projekt mit ähnlichem Namen existiert bereits. Was möchtest du tun?"
- Header: "Projekt"
- Options:
  1. "Bestehendes verwenden" - Use the existing project
  2. "Neues erstellen" - Create a new project with a different name
  3. "Setup abbrechen" - Cancel the setup

If user chooses "Bestehendes verwenden", skip to Phase 3 with the existing project.
If user chooses "Setup abbrechen", end the workflow with a friendly message.

### Step 2.3: Ask for Project Details

Use `AskUserQuestion` to confirm project details:
- Question: "Wie soll das Projekt heißen?"
- Header: "Projektname"
- Options:
  1. "[Directory Name]" (Recommended) - Use current directory name
  2. "[Framework] Project" - Use detected framework name

The user can also enter a custom name via "Other".

Then ask for the slug:
- Question: "Welches Kürzel soll für Tasks verwendet werden?"
- Header: "Slug"
- Options:
  1. "[First 2-3 letters uppercase]" (Recommended)
  2. Custom option via "Other"

### Step 2.4: Create Project

Use `mcp__thinkprompt__create_project` with:
- `name`: User's chosen project name
- `slug`: User's chosen slug (uppercase)
- `description`: Generated description based on detected stack, e.g., "Next.js 14 Projekt mit TypeScript, Tailwind CSS und Jest"

Output: "✅ Projekt **[Name]** ([SLUG]) erstellt"

Store the project ID for later use.

---

## Phase 3: Style Guide Setup

### Step 3.1: Check Existing Style Guides

Use `mcp__thinkprompt__list_templates` with `type: "style"` to find existing style guide templates.

Check if any templates match the detected framework/technologies:
- Match by `category` (e.g., "nextjs", "nestjs", "angular")
- Match by `title` containing framework name
- Match by `description` mentioning detected technologies

### Step 3.2: Ask User Preference

Use `AskUserQuestion`:
- Question: "Wie möchtest du den Style Guide einrichten?"
- Header: "Style Guide"
- Options:

**If matching templates found:**
1. "Template laden" (Recommended) - Use existing ThinkPrompt template
2. "Neu generieren" - Generate based on code analysis
3. "Überspringen" - Skip style guide creation

**If no matching templates:**
1. "Neu generieren" (Recommended) - Generate based on code analysis
2. "Überspringen" - Skip style guide creation

### Step 3.3a: Load Template (if "Template laden" chosen)

If multiple matching templates exist:
- Use `AskUserQuestion` to let user select
- Show template titles and descriptions as options

Use `mcp__thinkprompt__get_template` to load the selected template.

Output: "📚 Style Guide **[Template Title]** zugewiesen"

### Step 3.3b: Generate Style Guide (if "Neu generieren" chosen)

Analyze code patterns by reading a few representative files:

1. **File Structure:**
   - Check for `src/`, `app/`, `pages/`, `lib/`, `components/` directories
   - Document the folder organization

2. **Naming Conventions:**
   - File naming (kebab-case, camelCase, PascalCase)
   - Component naming
   - Function naming

3. **Import Patterns:**
   - Absolute vs relative imports
   - Import ordering (external → internal → types)
   - Barrel exports (index.ts)

4. **Code Patterns:**
   - Component structure (functional vs class)
   - State management patterns
   - Error handling patterns
   - API call patterns

5. **Testing Patterns:**
   - Test file location
   - Test naming conventions
   - Mocking patterns

Create the style guide using `mcp__thinkprompt__create_template`:
- `type`: "style"
- `title`: "[Framework] Style Guide - [ProjectName]"
- `category`: detected framework (lowercase, e.g., "nextjs", "nestjs")
- `content`: Generated markdown with the following structure:

```markdown
# [Framework] Style Guide - [ProjectName]

## Projektstruktur

[Detected folder structure]

## Namenskonventionen

### Dateien
- [Detected file naming pattern]

### Komponenten/Module
- [Detected component naming pattern]

### Funktionen & Variablen
- [Detected naming pattern]

## Import-Reihenfolge

1. External packages
2. Internal modules
3. Types/Interfaces
4. Styles

## Code-Patterns

### [Framework-specific patterns]
[Detected patterns with examples]

### Error Handling
[Detected error handling pattern]

### Testing
[Detected testing conventions]

## Zusätzliche Konventionen

[Any other detected patterns]
```

Output: "📚 Style Guide generiert basierend auf Code-Analyse"

### Step 3.4: Skip (if "Überspringen" chosen)

Output: "⏭️ Style Guide übersprungen"

---

## Phase 4: Create Prompts

### Step 4.1: Offer Prompt Selection

Use `AskUserQuestion` with `multiSelect: true`:
- Question: "Welche Prompts sollen erstellt werden?"
- Header: "Prompts"
- Options:
  1. "Code Review" - Strukturierte Code-Review Vorlage
  2. "Feature Planning" - Feature in Tasks aufteilen
  3. "Bug Report" - Bugs analysieren und dokumentieren
  4. "Commit Message" - Konsistente Commit Messages generieren

### Step 4.2: Create Selected Prompts

For each selected prompt, use `mcp__thinkprompt__create_prompt`:

**Code Review Prompt:**
```yaml
title: "Code Review - [ProjectName]"
description: "Strukturiertes Code Review mit Fokus auf Architektur, Sicherheit und Qualität"
content: |
  Führe ein Code Review für folgenden Code durch:

  ```
  {{code}}
  ```

  **Kontext:** {{context}}

  Analysiere:
  1. **Architektur & Design Patterns** - Passt der Code zur bestehenden Struktur?
  2. **Sicherheit** - OWASP Top 10, Input Validation, Authentication
  3. **Code-Qualität** - Lesbarkeit, Wartbarkeit, DRY-Prinzip
  4. **Error Handling** - Sind Fehler korrekt behandelt?
  5. **Performance** - Gibt es offensichtliche Performance-Probleme?

  Gib strukturiertes Feedback mit Prioritäten (Kritisch/Wichtig/Optional).
variables:
  - name: "code"
    type: "textarea"
    label: "Code"
    description: "Der zu überprüfende Code"
    required: true
  - name: "context"
    type: "text"
    label: "Kontext"
    description: "Zusätzlicher Kontext zum Code"
    required: false
```

**Feature Planning Prompt:**
```yaml
title: "Feature Planning - [ProjectName]"
description: "Feature in implementierbare Tasks aufteilen"
content: |
  Plane die Implementierung für folgendes Feature:

  **Feature:** {{feature}}

  **Anforderungen:**
  {{requirements}}

  Erstelle:
  1. **Task-Breakdown** - Kleine, schätzbare Tasks mit Abhängigkeiten
  2. **Technische Abhängigkeiten** - Welche Systeme/APIs sind betroffen?
  3. **Risikoanalyse** - Potenzielle Probleme und Mitigationen
  4. **Testplan** - Wie wird das Feature getestet?

  Format: Markdown mit klarer Struktur
variables:
  - name: "feature"
    type: "text"
    label: "Feature"
    description: "Name oder kurze Beschreibung des Features"
    required: true
  - name: "requirements"
    type: "textarea"
    label: "Anforderungen"
    description: "Detaillierte Anforderungen und Akzeptanzkriterien"
    required: true
```

**Bug Report Prompt:**
```yaml
title: "Bug Report - [ProjectName]"
description: "Bugs analysieren und Lösungen vorschlagen"
content: |
  Analysiere folgenden Bug:

  **Beschreibung:** {{description}}

  **Schritte zur Reproduktion:**
  {{steps}}

  **Erwartetes Verhalten:**
  {{expected}}

  Liefere:
  1. **Root Cause Analyse** - Was ist die wahrscheinliche Ursache?
  2. **Betroffene Code-Bereiche** - Welche Files/Funktionen sind betroffen?
  3. **Lösungsvorschlag** - Wie kann der Bug behoben werden?
  4. **Präventionsmaßnahmen** - Wie kann dieser Bug-Typ verhindert werden?
variables:
  - name: "description"
    type: "text"
    label: "Beschreibung"
    description: "Kurze Beschreibung des Bugs"
    required: true
  - name: "steps"
    type: "textarea"
    label: "Schritte zur Reproduktion"
    description: "Schritte um den Bug zu reproduzieren"
    required: true
  - name: "expected"
    type: "textarea"
    label: "Erwartetes Verhalten"
    description: "Was sollte eigentlich passieren?"
    required: true
```

**Commit Message Prompt:**
```yaml
title: "Commit Message - [ProjectName]"
description: "Konsistente Commit Messages im Conventional Commits Format"
content: |
  Generiere eine Commit Message für folgende Änderungen:

  **Typ:** {{type}}

  **Änderungen:**
  {{changes}}

  Format: Conventional Commits
  - Kurze Summary (max 72 Zeichen)
  - Leere Zeile
  - Detaillierte Beschreibung wenn nötig
  - Breaking Changes mit "BREAKING CHANGE:" markieren

  Beispiel:
  ```
  feat(auth): add OAuth2 login support

  - Add Google OAuth provider
  - Add GitHub OAuth provider
  - Update user model for external auth
  ```
variables:
  - name: "type"
    type: "select"
    label: "Typ"
    description: "Art der Änderung"
    required: true
    options:
      - "feat - Neues Feature"
      - "fix - Bug Fix"
      - "docs - Dokumentation"
      - "refactor - Code Refactoring"
      - "test - Tests"
      - "chore - Maintenance"
  - name: "changes"
    type: "textarea"
    label: "Änderungen"
    description: "Beschreibung der Änderungen"
    required: true
```

Output for each created prompt: "📝 Prompt **[Title]** erstellt"

After all prompts: "📝 [N] Prompts erstellt"

---

## Phase 5: Summary

Output final summary:

"🎉 **ThinkPrompt Setup abgeschlossen!**

**Projekt:** [ProjectName] ([SLUG])
**Style Guide:** [Style Guide Title or 'Keiner']
**Prompts:**
[List of created prompts with bullet points]

---

**Nächste Schritte:**
- `/feature-dev-tp` - Feature-Entwicklung mit automatischem Style Guide
- `/quality-analysis` - Code-Qualitätsanalyse mit Reporting
- Prompts in ThinkPrompt unter https://thinkprompt.app verwenden

Viel Erfolg mit deinem Projekt! 🚀"

---

## Error Handling

- **ThinkPrompt API nicht erreichbar:** Prüfe ob `/setup-thinkprompt` ausgeführt wurde
- **Kein Framework erkannt:** Generischen "Generic" Style Guide und Prompts anbieten
- **User bricht ab:** Freundliche Nachricht mit Hinweis auf erneuten Versuch
