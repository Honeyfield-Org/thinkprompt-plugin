---
description: Run comprehensive code quality analysis and store results in ThinkPrompt
argument-hint: Optional project ID or "quick" for fast analysis
---

# Quality Analysis

You are running a comprehensive code quality analysis. Execute local analysis tools, collect metrics, and store results in ThinkPrompt for trend tracking.

## Core Principles

- **Be thorough**: Run all applicable analysis tools for the project type
- **Handle errors gracefully**: If a tool isn't installed or fails, skip it and continue
- **Show progress**: Use TodoWrite to track each analysis phase
- **Provide actionable insights**: Highlight the most critical issues first

---

## Phase 1: Setup

**Goal**: Prepare for analysis

**Arguments**: $ARGUMENTS

**Actions**:
1. Create todo list with all analysis phases
2. Read `package.json` to detect project type and available scripts
3. Get git branch and commit info using `git rev-parse --abbrev-ref HEAD` and `git rev-parse HEAD`
4. List ThinkPrompt projects using `list_projects` MCP tool
5. If $ARGUMENTS contains a project ID, use that. Otherwise, ask user to select a project.
6. Start quality snapshot using `start_quality_analysis` with:
   - `projectId`: Selected project
   - `name`: "Quality Analysis - [branch] - [timestamp]"
   - `source`: "mcp"
   - `gitBranch`: Current branch
   - `gitCommit`: Current commit hash
7. Store the returned `snapshotId` for use in subsequent phases

---

## Phase 2: ESLint Analysis

**Goal**: Check code style and potential errors

**Actions**:
1. Check if ESLint is available: `npx eslint --version`
2. If available, run: `npx eslint . --format json --output-file /tmp/claude/eslint-report.json` (with appropriate ignore patterns)
3. Read and parse the JSON output
4. Count errors and warnings
5. Calculate score: `100 - (errors * 5 + warnings * 1)` (min 0)
6. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "eslint",
     "metricName": "ESLint Results",
     "value": { "errors": <count>, "warnings": <count>, "fixableErrors": <count>, "fixableWarnings": <count> },
     "score": <calculated_score>
   }
   ```
7. If there are issues (errors > 0), use `bulk_report_quality_issues` to report them:
   - Category: "lint"
   - Severity: "error" for errors, "warning" for warnings
   - Include file path, line number, rule ID

---

## Phase 3: TypeScript Analysis

**Goal**: Check type safety and coverage

**Actions**:
1. Check if TypeScript is configured: Look for `tsconfig.json`
2. Run type check: `npx tsc --noEmit 2>&1` and capture output
3. Parse output for errors (lines matching "error TS")
4. Count type errors
5. Optionally run type-coverage: `npx type-coverage --json` if available
6. Calculate score based on errors (0 errors = 100, each error = -5)
7. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "typescript",
     "metricName": "TypeScript Results",
     "value": { "errors": <count>, "coverage": <percentage if available> },
     "score": <calculated_score>
   }
   ```
8. Report any type errors as issues with category "type"

---

## Phase 4: Test Coverage

**Goal**: Measure test coverage

**Actions**:
1. Check if Jest is configured: Look for jest.config.* or "jest" in package.json
2. Run tests with coverage: `npm test -- --coverage --json --outputFile=/tmp/claude/jest-report.json` or `npx jest --coverage --json --outputFile=/tmp/claude/jest-report.json`
3. Parse coverage report from coverage/coverage-summary.json
4. Extract line, branch, function, and statement coverage percentages
5. Calculate overall coverage as average of all metrics
6. Score is the coverage percentage
7. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "test_coverage",
     "metricName": "Test Coverage",
     "value": {
       "lines": <percentage>,
       "branches": <percentage>,
       "functions": <percentage>,
       "statements": <percentage>,
       "passed": <count>,
       "failed": <count>,
       "skipped": <count>
     },
     "score": <overall_coverage>
   }
   ```
8. If tests failed, report them as issues with category "coverage"

---

## Phase 5: Complexity Analysis

**Goal**: Measure cyclomatic complexity

**Actions**:
1. Try running complexity analysis: `npx es6-plato -r -d /tmp/claude/plato-report src/` or `npx complexity-report --format json src/**/*.ts`
2. Alternative: Use a simpler heuristic by counting conditionals and loops in source files
3. Calculate average and max cyclomatic complexity
4. Score: 100 if avg < 5, 80 if avg < 10, 60 if avg < 15, 40 otherwise
5. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "cyclomatic_complexity",
     "metricName": "Code Complexity",
     "value": { "avgCyclomatic": <avg>, "maxCyclomatic": <max>, "highComplexityFiles": <count> },
     "score": <calculated_score>
   }
   ```
6. Report files with complexity > 15 as issues with category "complexity"

---

## Phase 6: Code Duplication

**Goal**: Detect duplicate code

**Actions**:
1. Run jscpd: `npx jscpd --reporters json --output /tmp/claude/jscpd-report src/`
2. Parse the JSON report
3. Calculate duplication percentage
4. Score: 100 - (duplication_percentage * 2), min 0
5. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "code_duplication",
     "metricName": "Code Duplication",
     "value": { "percentage": <percentage>, "duplicatedLines": <count>, "clones": <count> },
     "score": <calculated_score>
   }
   ```
6. Report significant duplications (>10 lines) as issues with category "duplication"

---

## Phase 7: Bundle Size (Optional)

**Goal**: Measure build output size

**Skip if**: No build script in package.json or not a frontend project

**Actions**:
1. Check for build script in package.json
2. Run build: `npm run build`
3. Measure output size: `du -sh dist/ build/` or analyze webpack stats
4. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "bundle_size",
     "metricName": "Bundle Size",
     "value": { "totalSizeKb": <size>, "mainChunkKb": <size if available> },
     "score": <based on size thresholds>
   }
   ```

---

## Phase 8: Dependency Check

**Goal**: Check for vulnerabilities and outdated packages

**Actions**:
1. Run npm audit: `npm audit --json 2>/dev/null`
2. Parse vulnerabilities by severity
3. Run npm outdated: `npm outdated --json 2>/dev/null`
4. Count outdated packages
5. Score: 100 - (critical * 20 + high * 10 + moderate * 5 + low * 1 + outdated * 2)
6. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "dependency_health",
     "metricName": "Dependency Health",
     "value": {
       "vulnerabilities": { "critical": <n>, "high": <n>, "moderate": <n>, "low": <n> },
       "outdated": <count>,
       "total": <total_deps>
     },
     "score": <calculated_score>
   }
   ```
7. Report critical and high vulnerabilities as issues with category "dependency" and severity "error"

---

## Phase 9: Dead Code Detection

**Goal**: Find unused exports and unreachable code

**Actions**:
1. Try ts-prune: `npx ts-prune 2>/dev/null | head -100`
2. Alternative: Try knip: `npx knip --reporter json 2>/dev/null`
3. Count unused exports
4. Score: 100 - (unused_exports * 2), min 50
5. Record metric using `record_quality_metric`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "metricType": "dead_code",
     "metricName": "Dead Code",
     "value": { "unusedExports": <count>, "unusedFiles": <count if available> },
     "score": <calculated_score>
   }
   ```
6. Report unused exports as issues with category "dead_code" and severity "info"

---

## Phase 10: Completion

**Goal**: Finalize analysis and present results

**Actions**:
1. Complete the snapshot using `complete_quality_analysis`:
   ```json
   {
     "snapshotId": "<snapshotId>",
     "status": "completed",
     "notes": "Analysis completed successfully"
   }
   ```
2. Retrieve the summary from the response
3. Get quality overview using `get_quality_overview` with projectId
4. Present results to user:
   - Overall score with trend (compared to previous snapshot)
   - Breakdown by metric type
   - Top 5-10 most critical issues
   - Recommendations for improvement
5. Mark all todos as complete

---

## Quick Mode

If $ARGUMENTS contains "quick":
- Skip Phase 5 (Complexity)
- Skip Phase 6 (Duplication)
- Skip Phase 7 (Bundle Size)
- Skip Phase 9 (Dead Code)
- Only run ESLint, TypeScript, Test Coverage, and Dependency Check

---

## Error Handling

If any tool fails or isn't installed:
1. Log the error
2. Skip that phase
3. Continue with remaining phases
4. Note skipped phases in the final summary

---

## Output Format

Present results in a clear, scannable format:

```
## Quality Analysis Results

**Overall Score**: 82/100 (up from 78)

### Metrics
| Metric | Score | Details |
|--------|-------|---------|
| ESLint | 90 | 2 errors, 8 warnings |
| TypeScript | 100 | 0 errors |
| Test Coverage | 75 | 75% line coverage |
| Complexity | 80 | Avg: 4.2, Max: 12 |
| Duplication | 88 | 3.2% duplicated |
| Dependencies | 70 | 2 vulnerabilities, 5 outdated |
| Dead Code | 85 | 8 unused exports |

### Top Issues
1. [ERROR] src/auth/login.ts:45 - @typescript-eslint/no-unused-vars
2. [ERROR] npm audit - lodash has critical vulnerability
3. [WARNING] src/utils/helpers.ts - Cyclomatic complexity 15
...

### Recommendations
1. Fix the 2 ESLint errors (auto-fixable)
2. Update lodash to patch critical vulnerability
3. Add tests to improve coverage from 75% to 80%
```
