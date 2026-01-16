---
description: Feature development with automatic Style Guide loading from ThinkPrompt
argument-hint: <feature-description>
---

# Feature Development with ThinkPrompt Style Guides

You are implementing a feature using the feature-dev workflow, enhanced with automatic style guide loading from ThinkPrompt.

## Pre-Phase: Style Guide Loading

**CRITICAL: Before starting any feature development, you MUST load the appropriate style guide.**

### Step 1: Detect Project Type

Run the project detection script to determine the framework:

```bash
~/.claude/plugins/local/thinkprompt/scripts/detect-project-type.sh .
```

Or manually check for:
- **Next.js**: `next.config.*` file OR `"next"` in package.json dependencies
- **NestJS**: `nest-cli.json` file OR `"@nestjs/core"` in package.json dependencies

### Step 2: Load Style Guide Template

Based on the detected project type, load the corresponding style guide:

**For Next.js projects:**
Use `mcp__thinkprompt__get_template` with id: `74df9ecd-57a1-46fa-aea8-e957561508c7`

**For NestJS projects:**
Use `mcp__thinkprompt__get_template` with id: `388b08ca-0cc9-4447-a336-64223b9f06a8`

**For unknown projects:**
Skip style guide loading and proceed with generic best practices.

### Step 3: Acknowledge Style Guide

After loading, output:
```
📚 Loaded Style Guide: [Template Title]
Framework: [nextjs/nestjs]
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

### For Next.js Projects
- [ ] Using App Router patterns (`src/app/`)
- [ ] Server Components by default, `'use client'` only when needed
- [ ] React Query with query key factory pattern
- [ ] Zustand stores with selector hooks
- [ ] Type imports separated (`import type { ... }`)
- [ ] Path alias `@/*` used consistently
- [ ] Tailwind classes properly sorted
- [ ] Error boundaries where needed

### For NestJS Projects
- [ ] One module per domain/feature
- [ ] Controllers thin, logic in services
- [ ] DTOs with class-validator decorators
- [ ] Proper exception handling
- [ ] Repository pattern for data access
- [ ] Unit tests with mocked dependencies

---

## Feature Request

**Implementing:** `$ARGUMENTS`

Begin with Phase 0 (Style Guide Loading), then proceed through all phases systematically.
