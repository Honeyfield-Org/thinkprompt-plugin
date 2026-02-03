---
name: Feature Workflow
description: This skill should be used when the user asks "how does feature development work", "what's the workflow", "how do I start a feature", "ThinkPrompt workflow", "feature to tasks", or needs guidance on the end-to-end development process from feature creation through code review and quality analysis.
---

# Feature Development Workflow

## Wann diesen Guide nutzen

- User startet ein neues Feature
- User fragt nach dem Entwicklungsprozess
- User will verstehen wie die ThinkPrompt-Tools zusammenarbeiten
- User plant eine größere Implementierung

---

## Workflow-Übersicht

```
┌─────────────────┐
│  1. Setup       │  /setup-workspace (einmalig pro Projekt)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Feature     │  Feature in ThinkPrompt anlegen
│     anlegen     │  (manuell oder via generate_features_from_document)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Tasks       │  /feature-dev-tp oder generate_tasks_from_feature
│     generieren  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Entwicklung │  Tasks abarbeiten mit Style Guide
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. Review      │  code-reviewer Agent
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. Quality     │  /quality-analysis
│     Check       │
└─────────────────┘
```

---

## Phase 1: Projekt-Setup (einmalig)

### Schritt 1.1: API-Key konfigurieren
```
/setup-thinkprompt
```
- API-Key eingeben
- Claude Code neu starten

### Schritt 1.2: Workspace einrichten
```
/setup-workspace
```
- Projekt wird analysiert
- ThinkPrompt-Projekt wird erstellt
- Style Guide wird generiert/geladen
- Standard-Prompts werden erstellt

**Ergebnis:** Projekt mit Style Guide und Prompts in ThinkPrompt

---

## Phase 2: Feature anlegen

### Option A: Manuell in ThinkPrompt
1. https://thinkprompt.ai öffnen
2. Projekt auswählen
3. Feature erstellen mit:
   - Name
   - Beschreibung
   - Status: `new` → `rfc` → `approved` → `ready_for_dev`

### Option B: Via MCP Tool
```
mcp__thinkprompt__create_feature({
  projectId: "...",
  name: "User Authentication",
  description: "OAuth2 Login mit Google und GitHub",
  status: "new"
})
```

### Option C: Aus Dokument generieren
```
mcp__thinkprompt__generate_features_from_document({
  projectId: "...",
  document: "[Meeting Notes oder Spec]"
})
```

### Feature-Status Workflow

```
new → rfc → approved → blocked → ready_for_dev → ready_for_review → done
 │     │       │          │            │                │            │
 │     │       │          │            │                │            └─ Fertig!
 │     │       │          │            │                └─ Code Review
 │     │       │          │            └─ Entwicklung startet
 │     │       │          └─ Blockiert (Abhängigkeiten)
 │     │       └─ Genehmigt
 │     └─ Request for Comments
 └─ Neu erstellt
```

---

## Phase 3: Tasks generieren

### Mit /feature-dev-tp (empfohlen)
```
/feature-dev-tp
```
- Lädt automatisch den Style Guide
- Analysiert die Codebase
- Generiert passende Tasks
- Berücksichtigt bestehende Patterns

### Direkt via MCP
```
mcp__thinkprompt__generate_tasks_from_feature({
  featureId: "...",
  additionalContext: "Next.js 14 App Router, Prisma ORM"
})
```

**Voraussetzung:** Feature muss Status `ready_for_dev` haben

### Task-Eigenschaften

| Feld | Beschreibung |
|------|--------------|
| `title` | Kurzer, klarer Titel |
| `description` | Was getan werden soll |
| `content` | Details, SQL, Specs |
| `complexity` | trivial/low/medium/high/critical |
| `priority` | low/medium/high/urgent |
| `estimationHours` | Geschätzte Stunden |

---

## Phase 4: Entwicklung

### Task starten
```
mcp__thinkprompt__update_task_status({
  id: "task-id",
  status: "in_progress"
})
```

### Mit Style Guide arbeiten
Der Style Guide wird automatisch vom `code-reviewer` und `/feature-dev-tp` geladen.

**Manuelle Style Guide Nutzung:**
```
mcp__thinkprompt__list_templates({ type: "style" })
mcp__thinkprompt__get_template({ id: "..." })
```

### Task abschließen
```
mcp__thinkprompt__update_task_status({
  id: "task-id",
  status: "done"
})
```

---

## Phase 5: Code Review

### Automatisch via Agent
Der `code-reviewer` Agent wird automatisch getriggert wenn:
- Du sagst "Ich bin fertig mit..."
- Du um ein Review bittest
- Du eine Implementierung abschließt

### Manuell triggern
```
"Bitte reviewe den Code den ich gerade geschrieben habe"
```

### Was der Code Reviewer macht
1. Lädt passenden Style Guide aus ThinkPrompt
2. Analysiert den Code
3. Prüft auf:
   - Style Guide Compliance
   - Architektur-Patterns
   - Security Issues
   - Code Quality
4. Gibt strukturiertes Feedback

---

## Phase 6: Quality Check

### Quality Analysis starten
```
/quality-analysis
```

### Was geprüft wird
- ESLint Errors/Warnings
- TypeScript Strict Mode
- Test Coverage
- Code Duplication
- Cyclomatic Complexity
- Bundle Size
- Dead Code

### Ergebnisse in ThinkPrompt
- Snapshot wird erstellt
- Issues werden dokumentiert
- Trends über Zeit sichtbar

---

## Schnellreferenz: Welches Tool wann?

| Aufgabe | Tool/Command |
|---------|--------------|
| Erstes Setup | `/setup-thinkprompt` → `/setup-workspace` |
| Neues Feature starten | `/feature-dev-tp` |
| Tasks generieren | `/feature-dev-tp` oder MCP |
| Code schreiben | Normal entwickeln |
| Code reviewen | `code-reviewer` Agent (automatisch) |
| Qualität prüfen | `/quality-analysis` |
| Feature-Status ändern | MCP `update_feature_status` |
| Task-Status ändern | MCP `update_task_status` |

---

## Best Practices

### 1. Features klein halten
- Ein Feature = 3-7 Tasks
- Zu große Features aufteilen

### 2. Tasks schätzbar machen
- Max 1 Tag pro Task
- Klare Akzeptanzkriterien

### 3. Style Guide nutzen
- Einmal pro Projekt einrichten
- Bei Bedarf anpassen

### 4. Regelmäßig Quality Checks
- Vor jedem PR
- Mindestens wöchentlich

### 5. Status aktuell halten
- Tasks und Features updaten
- Blockaden dokumentieren

---

## Troubleshooting

### "ThinkPrompt API nicht erreichbar"
→ `/setup-thinkprompt` ausführen und Claude Code neu starten

### "Kein Style Guide gefunden"
→ `/setup-workspace` ausführen oder manuell Template erstellen

### "Feature hat keine Tasks"
→ Feature-Status auf `ready_for_dev` setzen, dann Tasks generieren

### "Tasks werden nicht generiert"
→ Feature braucht Status `ready_for_dev` UND darf keine bestehenden Tasks haben
