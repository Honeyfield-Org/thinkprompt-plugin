---
description: Best practices for creating effective prompts in ThinkPrompt. Use when user wants to create, improve, or understand prompts and templates.
---

# Prompt Engineering mit ThinkPrompt

## Wann diesen Guide nutzen

- User will einen neuen Prompt erstellen
- User will einen bestehenden Prompt verbessern
- User fragt nach Prompt Best Practices
- User erstellt Templates

---

## Prompt-Struktur

Ein guter ThinkPrompt-Prompt folgt dieser Struktur:

```
1. Klare Aufgabenstellung (Was soll getan werden?)
2. Kontext-Variablen (Eingaben vom User)
3. Erwartetes Output-Format (Wie soll die Antwort aussehen?)
4. Constraints/Regeln (Was soll beachtet werden?)
```

### Beispiel

```markdown
Analysiere folgenden Code auf Sicherheitsprobleme:

```
{{code}}
```

**Kontext:** {{context}}

Prüfe auf:
1. SQL Injection
2. XSS Vulnerabilities
3. Authentication Bypass
4. Sensitive Data Exposure

Output-Format:
- Severity (Critical/High/Medium/Low)
- Betroffene Zeile(n)
- Beschreibung des Problems
- Lösungsvorschlag
```

---

## Variablen-Typen

ThinkPrompt unterstützt diese Variablen-Typen:

| Typ | Verwendung | Beispiel |
|-----|------------|----------|
| `text` | Kurze Eingaben (1 Zeile) | Feature-Name, Titel |
| `textarea` | Längere Eingaben (mehrzeilig) | Code, Beschreibungen |
| `number` | Numerische Werte | Priorität, Schätzung |
| `select` | Vordefinierte Optionen | Typ-Auswahl, Kategorie |
| `date` | Datumswerte | Deadline, Sprint-Ende |
| `boolean` | Ja/Nein Entscheidungen | Feature-Flags |

### Best Practices für Variablen

1. **Sinnvolle Namen:** `feature_name` statt `input1`
2. **Klare Labels:** "Feature-Name" statt "Name"
3. **Hilfreiche Descriptions:** Erkläre was erwartet wird
4. **Default-Werte:** Wo sinnvoll, Defaults setzen
5. **Required nur wenn nötig:** Nicht alles muss Pflicht sein

---

## Prompt-Typen

### 1. Analyse-Prompts
Für Code-Review, Bug-Analyse, Security-Checks.

**Struktur:**
```
Input: [Was analysiert werden soll]
Fokus: [Worauf achten]
Output: [Strukturiertes Ergebnis]
```

### 2. Generierungs-Prompts
Für Code-Generierung, Dokumentation, Tests.

**Struktur:**
```
Aufgabe: [Was generiert werden soll]
Kontext: [Bestehendes System, Constraints]
Format: [Sprache, Style, Patterns]
```

### 3. Transformations-Prompts
Für Refactoring, Migration, Konvertierung.

**Struktur:**
```
Input: [Ursprünglicher Code/Text]
Ziel: [Gewünschtes Format/Pattern]
Regeln: [Was beibehalten, was ändern]
```

### 4. Planungs-Prompts
Für Feature-Planning, Task-Breakdown, Architektur.

**Struktur:**
```
Ziel: [Was erreicht werden soll]
Constraints: [Zeit, Ressourcen, Tech-Stack]
Output: [Plan-Format, Granularität]
```

---

## Templates vs Prompts

| Aspekt | Prompt | Template |
|--------|--------|----------|
| **Zweck** | Wiederverwendbare Aufgabe | Style Guide / Beispiel |
| **Variablen** | Ja, mit `{{var}}` | Nein |
| **Typ** | - | `example` oder `style` |
| **Verwendung** | Direkte Ausführung | Kontext/Referenz |

### Template-Typen

- **`example`**: Beispiel-Prompts als Inspiration
- **`style`**: Style Guides für Code-Standards

---

## Anti-Patterns vermeiden

### ❌ Zu vage
```
Schreibe guten Code für {{feature}}
```

### ✅ Besser: Spezifisch
```
Implementiere {{feature}} als React-Komponente mit:
- TypeScript strict mode
- Unit Tests mit Jest
- Error Boundary
- Loading/Error States
```

### ❌ Zu viele Variablen
```
{{a}} {{b}} {{c}} {{d}} {{e}} {{f}} {{g}}
```

### ✅ Besser: Gruppierte Eingaben
```
**Feature:** {{feature_name}}
**Anforderungen:** {{requirements}}
```

### ❌ Kein Output-Format
```
Analysiere den Code
```

### ✅ Besser: Klares Format
```
Analysiere den Code und gib aus:
1. **Summary**: 2-3 Sätze
2. **Issues**: Tabelle mit Severity/Location/Fix
3. **Empfehlungen**: Priorisierte Liste
```

---

## ThinkPrompt API nutzen

### Prompt erstellen
```
mcp__thinkprompt__create_prompt({
  title: "Code Review",
  description: "Strukturiertes Code Review",
  content: "...",
  variables: [
    { name: "code", type: "textarea", required: true },
    { name: "context", type: "text", required: false }
  ]
})
```

### Template erstellen
```
mcp__thinkprompt__create_template({
  title: "React Style Guide",
  type: "style",
  category: "react",
  content: "...",
  useCaseHints: ["React components", "Frontend code"]
})
```

---

## Checkliste für gute Prompts

- [ ] Klare, spezifische Aufgabenstellung
- [ ] Sinnvolle Variablen mit guten Namen/Labels
- [ ] Definiertes Output-Format
- [ ] Constraints und Regeln wo nötig
- [ ] Beispiele bei komplexen Anforderungen
- [ ] Nicht zu lang (fokussiert bleiben)
