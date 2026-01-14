# Quality Analysis Plugin for Claude Code

A comprehensive code quality analysis skill that runs local analysis tools and stores results in ThinkPrompt for trend tracking.

## Usage

```bash
# Full analysis
/quality-analysis

# Quick analysis (core metrics only)
/quality-analysis quick

# Analyze specific project
/quality-analysis <project-id>
```

## Metrics Analyzed

| Metric | Tool | What it measures |
|--------|------|------------------|
| ESLint | eslint | Code style and potential errors |
| TypeScript | tsc, type-coverage | Type errors and type coverage |
| Test Coverage | jest | Line, branch, function coverage |
| Complexity | es6-plato | Cyclomatic complexity |
| Duplication | jscpd | Copy-pasted code |
| Bundle Size | webpack stats | Build output size |
| Dependencies | npm audit/outdated | Vulnerabilities and outdated packages |
| Dead Code | ts-prune, knip | Unused exports and files |

## Requirements

- Node.js project with `package.json`
- ThinkPrompt MCP server connected
- Git repository (for branch/commit tracking)

## How It Works

1. **Setup**: Detects project type, gets git info, creates quality snapshot in ThinkPrompt
2. **Analysis**: Runs each applicable tool and parses results
3. **Recording**: Stores metrics and issues via ThinkPrompt MCP tools
4. **Summary**: Presents overall score with trends and recommendations

## Quick Mode

Use `/quality-analysis quick` to skip:
- Complexity analysis
- Duplication detection
- Bundle size analysis
- Dead code detection

Only runs: ESLint, TypeScript, Test Coverage, Dependency Check

## Scoring

Each metric produces a score from 0-100. The overall score is a weighted average:
- ESLint: 15%
- TypeScript: 15%
- Test Coverage: 20%
- Complexity: 10%
- Duplication: 10%
- Dependencies: 15%
- Dead Code: 5%
- Bundle Size: 10%

## ThinkPrompt Integration

Results are stored in ThinkPrompt allowing:
- Trend analysis over time
- Comparison between snapshots
- Issue tracking and resolution
- Team visibility into code health

## Author

Honeyfield (dev@honeyfield.de)
