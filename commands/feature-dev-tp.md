---
description: Feature development with automatic Style Guide loading from ThinkPrompt
argument-hint: <feature-description>
---

# Feature Development with ThinkPrompt Style Guides

You are implementing a feature using the feature-dev workflow, enhanced with automatic style guide loading from ThinkPrompt.

## Pre-Phase: Style Guide Loading

**CRITICAL: Before starting any feature development, you MUST attempt to load the appropriate style guide.**

### Step 1: Load Available Style Guides

Use `mcp__thinkprompt__list_templates` with `type: "style"` to get all available style guide templates.
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
- Automatically load the template using `mcp__thinkprompt__get_template` with the template's `id`
- Output: "📚 Loaded Style Guide: [Template Title]"

**Multiple matches:**
- Use the `AskUserQuestion` tool to let the user choose:
  - Question: "Mehrere Style Guides passen zu deinem Projekt. Welchen möchtest du verwenden?"
  - Header: "Style Guide"
  - Options: List each matching template with its title as label and description
  - Add a final option: "Keinen verwenden" / "None"
- Load the selected template using `mcp__thinkprompt__get_template`, or skip if user chose "None"

### Step 5: Acknowledge Style Guide

After loading (if a template was selected), output:
```
📚 Loaded Style Guide: [Template Title]
Category: [template.category]
```

Keep the style guide content in context for ALL subsequent phases.

---

## Feature Development Workflow (7 Phases)

Now proceed with the standard feature-dev workflow, applying the loaded style guide conventions throughout.

### Phase 1: Understanding & Clarification

1. **Read and understand** the feature request: `$ARGUMENTS`
2. **Ask clarifying questions** if requirements are ambiguous
3. **Identify scope boundaries** - what's in/out of scope
4. **Check for dependencies** on other features or systems

### Phase 2: Codebase Exploration

1. **Explore relevant parts** of the codebase using the Task tool with `subagent_type=Explore`
2. **Identify existing patterns** that should be followed (per the style guide)
3. **Find related code** that the new feature will interact with
4. **Note architectural decisions** already made in the project

### Phase 3: Architecture Design

1. **Design the feature architecture** following the style guide patterns
2. **Identify files to create/modify**
3. **Define data structures** (types, interfaces, DTOs)
4. **Plan component hierarchy** (for frontend) or module structure (for backend)
5. **Consider edge cases** and error handling

### Phase 4: Implementation Planning

1. **Break down into small, testable tasks**
2. **Use TodoWrite** to track all implementation tasks
3. **Order tasks** by dependencies
4. **Identify potential blockers**

### Phase 5: Implementation

1. **Implement one task at a time**
2. **Follow the style guide** for:
   - File organization
   - Naming conventions
   - Code patterns (hooks, stores, services, DTOs, etc.)
   - Import ordering
   - Error handling
3. **Mark tasks complete** as you finish them
4. **Test as you go** when possible

### Phase 6: Integration & Testing

1. **Verify the feature works end-to-end**
2. **Check for TypeScript errors**: `pnpm typecheck` or `npm run lint`
3. **Run existing tests** to ensure no regressions
4. **Manual testing** of the new functionality

### Phase 7: Review & Polish

1. **Review code against the style guide**
2. **Clean up any TODO comments**
3. **Ensure consistent formatting**
4. **Remove debug code**
5. **Summarize what was implemented**

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

Begin with the Pre-Phase (Style Guide Loading), then proceed through all 7 phases systematically.
