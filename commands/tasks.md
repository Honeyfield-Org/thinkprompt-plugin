---
description: View and manage ThinkPrompt tasks for your project
argument-hint: "[status|kürzel|search term]"
---

# ThinkPrompt Task Management

Du hilfst dem User bei der Verwaltung von Tasks in ThinkPrompt.

---

## Phase 1: Projekt ermitteln

### Schritt 1.1: Projekte laden

Verwende `mcp__thinkprompt__list_projects` um alle Projekte zu laden.

### Schritt 1.2: Projekt matchen

Versuche das aktuelle Projekt automatisch zu finden:

1. **Verzeichnisname prüfen:** Vergleiche den aktuellen Verzeichnisnamen mit Projektnamen
2. **Package.json prüfen:** Falls vorhanden, `name` Feld mit Projektnamen vergleichen
3. **Slug prüfen:** Schaue ob ein Projekt-Slug zum Verzeichnis passt

### Schritt 1.3: Bei Mehrdeutigkeit fragen

Falls kein eindeutiges Projekt gefunden oder mehrere passen:

Verwende `AskUserQuestion`:
- Question: "Für welches Projekt möchtest du Tasks sehen?"
- Header: "Projekt"
- Options: Liste der Projekte mit Name und Slug

---

## Phase 2: Argument verarbeiten

Prüfe `$ARGUMENTS`:

### Fall A: Kein Argument
→ Zeige Task-Übersicht (Phase 3)

### Fall B: Status-Filter
Erkenne Status-Keywords:
- `open`, `offen` → status: "open"
- `in_progress`, `in-progress`, `wip` → status: "in_progress"
- `blocked`, `blockiert` → status: "blocked"
- `review` → status: "review"
- `done`, `fertig`, `erledigt` → status: "done"

→ Zeige gefilterte Tasks (Phase 3 mit Filter)

### Fall C: Kürzel (z.B. "TP-042")
Wenn Argument dem Pattern `[A-Z]+-\d+` entspricht:

→ Zeige Task-Details (Phase 4)

### Fall D: Suchbegriff
Alles andere als Suchbegriff behandeln:

→ Suche Tasks (Phase 3 mit search)

---

## Phase 3: Task-Übersicht

### Schritt 3.1: Tasks laden

Verwende `mcp__thinkprompt__list_tasks` mit:
- `projectId`: Ermitteltes Projekt
- `status`: Falls Filter aus Phase 2
- `search`: Falls Suchbegriff aus Phase 2
- `limit`: 20

### Schritt 3.2: Übersicht formatieren

Zeige die Tasks gruppiert nach Status:

```
📋 **Tasks für [Projektname]**

**🔴 Blockiert** (X)
| Kürzel | Titel | Priorität |
|--------|-------|-----------|
| TP-005 | Fix auth bug | high |

**🟡 In Arbeit** (X)
| Kürzel | Titel | Priorität |
|--------|-------|-----------|
| TP-012 | Implement login | medium |

**⚪ Offen** (X)
| Kürzel | Titel | Priorität |
|--------|-------|-----------|
| TP-015 | Add tests | low |
| TP-016 | Update docs | low |

**🟢 Erledigt** (X kürzlich)
| Kürzel | Titel |
|--------|-------|
| TP-010 | Setup project |

---
Gesamt: X offen, X in Arbeit, X blockiert, X erledigt

💡 `/tasks TP-012` für Details | `/tasks open` für Filter
```

### Schritt 3.3: Bei vielen Tasks

Falls mehr als 20 Tasks:
- Zeige Pagination-Hinweis
- Empfehle Filter: `/tasks open` oder `/tasks [suchbegriff]`

---

## Phase 4: Task-Details

### Schritt 4.1: Task laden

Verwende `mcp__thinkprompt__get_task` mit:
- `kuerzel`: Das Kürzel aus dem Argument

### Schritt 4.2: Details anzeigen

```
📌 **[Kürzel] [Titel]**

**Status:** [Status-Emoji] [Status]
**Priorität:** [Priorität]
**Komplexität:** [Komplexität]
**Geschätzt:** [X Stunden]
**Feature:** [Feature-Name] (falls zugeordnet)

---

**Beschreibung:**
[description]

**Details:**
[content - falls vorhanden]

---

**Tags:** [tag1], [tag2]
**Erstellt:** [Datum]
**Aktualisiert:** [Datum]
```

### Schritt 4.3: Aktionen anbieten

Verwende `AskUserQuestion`:
- Question: "Was möchtest du mit diesem Task tun?"
- Header: "Aktion"
- Options:
  1. "Status ändern" - Task-Status aktualisieren
  2. "Kommentar hinzufügen" - Notiz hinterlassen
  3. "History anzeigen" - Änderungshistorie
  4. "Nichts" - Zurück zur Übersicht

---

## Phase 5: Aktionen ausführen

### Aktion: Status ändern

Verwende `AskUserQuestion`:
- Question: "Welchen Status soll der Task haben?"
- Header: "Status"
- Options:
  1. "⚪ Offen" → "open"
  2. "🟡 In Arbeit" → "in_progress"
  3. "🔴 Blockiert" → "blocked"
  4. "🔵 Review" → "review"
  5. "🟢 Erledigt" → "done"

Dann `mcp__thinkprompt__update_task_status` mit neuem Status.

Output: "✅ Task [Kürzel] auf **[Status]** gesetzt"

### Aktion: Kommentar hinzufügen

Verwende `AskUserQuestion`:
- Question: "Welchen Kommentar möchtest du hinzufügen?"
- Header: "Kommentar"
- Options: (User wählt "Other" für Texteingabe)

Dann `mcp__thinkprompt__add_task_comment` mit dem Kommentar.

Output: "💬 Kommentar zu [Kürzel] hinzugefügt"

### Aktion: History anzeigen

Verwende `mcp__thinkprompt__get_task_history`.

Zeige Änderungen:
```
📜 **History für [Kürzel]**

| Datum | Änderung | Von → Nach |
|-------|----------|------------|
| 27.01. | Status | open → in_progress |
| 26.01. | Erstellt | - |
```

---

## Schnellbefehle

Informiere den User über verfügbare Shortcuts:

| Befehl | Beschreibung |
|--------|--------------|
| `/tasks` | Alle Tasks anzeigen |
| `/tasks open` | Nur offene Tasks |
| `/tasks wip` | Tasks in Arbeit |
| `/tasks blocked` | Blockierte Tasks |
| `/tasks done` | Erledigte Tasks |
| `/tasks TP-042` | Task-Details |
| `/tasks login` | Tasks suchen |

---

## Error Handling

### Kein Projekt gefunden
"⚠️ Kein ThinkPrompt-Projekt gefunden. Führe `/setup-workspace` aus, um ein Projekt anzulegen."

### Task nicht gefunden
"⚠️ Task [Kürzel] nicht gefunden. Prüfe das Kürzel oder verwende `/tasks` für eine Übersicht."

### API-Fehler
"⚠️ ThinkPrompt API nicht erreichbar. Prüfe ob `/setup-thinkprompt` ausgeführt wurde."
