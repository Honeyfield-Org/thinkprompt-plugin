# ThinkPrompt Plugin for Claude Code

Integrate ThinkPrompt's powerful prompt management, project tracking, quality analytics, and test session tools directly into Claude Code.

## Features

### 📝 Prompt Management
- Create, manage, and execute prompts with variables
- Browse and use templates (example prompts and style guides)
- Version control for prompts
- Tag-based organization

### 📊 Project & Task Management
- Manage projects, features/epics, and tasks
- Hierarchical feature structure (Epic → Story → Task)
- AI-powered task generation from features
- Comment threads and change history
- Kürzel-based task references (e.g., "TP-001")

### 🔄 Workflow Automation
- Create reusable automation sequences
- Combine prompts, templates, and tasks
- Conditional execution and error handling
- Track workflow execution history

### 🔍 Quality Analytics
- Comprehensive code quality analysis with `/quality-analysis` command
- Track ESLint, TypeScript, test coverage, complexity, duplication
- Store results in ThinkPrompt for trend tracking
- Issue tracking with severity and location
- Dashboard with scores and trends over time

### 🧪 Test Analytics
- Track QA and Playwright testing sessions
- Log network requests, console messages, interactions
- Report bugs with screenshots and environment info
- Session summaries with metrics and issue breakdown

### 🔌 Plugin Marketplace
- Browse and install Claude Code plugins
- Search by category and keywords
- Track plugin installations and ratings

## Installation

### Prerequisites
- Claude Code installed
- Node.js 18+ (for MCP server via npx)
- ThinkPrompt account with API key

### Install Plugin

```bash
claude plugin install bitbucket:vernes_p/thinkprompt-plugin
```

### Configure API Key

Add the environment variables to your Claude Code settings file `~/.claude/settings.json`:

```json
{
  "env": {
    "THINKPROMPT_API_URL": "https://thinkprompt-api-v2.azurewebsites.net/api/v1",
    "THINKPROMPT_API_KEY": "tp_your-api-key-here"
  }
}
```

**Important:** Claude Code does NOT automatically load `.env` files. Environment variables must be configured in `settings.json`.

Get your API key from: https://thinkprompt.app/settings/api-keys

For local development, use:
```json
{
  "env": {
    "THINKPROMPT_API_URL": "http://localhost:3001/api/v1",
    "THINKPROMPT_API_KEY": "tp_your-api-key-here"
  }
}
```

### Verify Installation

Restart Claude Code and check that ThinkPrompt MCP tools are available:
- `list_prompts`
- `list_projects`
- `start_quality_analysis`
- etc.

## Commands

### `/quality-analysis`

Run comprehensive code quality analysis and store results in ThinkPrompt.

```bash
# Full analysis
/quality-analysis

# Quick mode (core metrics only)
/quality-analysis quick

# Analyze specific project
/quality-analysis <project-id>
```

**Metrics analyzed:**
- ESLint (code style and errors)
- TypeScript (type errors)
- Test Coverage (line, branch, function)
- Cyclomatic Complexity
- Code Duplication
- Bundle Size
- Dependencies (vulnerabilities, outdated)
- Dead Code (unused exports)

## MCP Tools

The plugin provides 70+ MCP tools via the ThinkPrompt MCP Server:

### Prompt Tools
`list_prompts`, `get_prompt`, `create_prompt`, `update_prompt`, `execute_prompt`, `get_prompt_variables`

### Template Tools
`list_templates`, `get_template`, `create_template`, `update_template`

### Project Tools
`list_projects`, `get_project`, `create_project`, `get_project_statistics`

### Feature Tools
`list_features`, `create_feature`, `update_feature_status`, `add_feature_comment`, `get_feature_history`

### Task Tools
`list_tasks`, `get_task`, `create_task`, `update_task`, `update_task_status`, `ai_edit_task`, `add_task_comment`, `get_task_history`

### AI Generation Tools
`generate_tasks_from_feature`, `generate_tasks_bulk`, `generate_features_from_document`

### Workflow Tools
`list_workflows`, `get_workflow`, `create_workflow`, `update_workflow`, `delete_workflow`, `validate_workflow`

### Quality Analytics Tools
`start_quality_analysis`, `record_quality_metric`, `report_quality_issue`, `complete_quality_analysis`, `get_quality_overview`, `get_quality_trends`

### Test Analytics Tools
`start_test_session`, `record_metric`, `report_issue`, `end_test_session`, `list_test_sessions`, `get_test_session`

### Workspace Tools
`list_workspaces`, `get_current_workspace`, `switch_workspace`

### Plugin Marketplace Tools
`search_marketplace_plugins`, `get_marketplace_plugin`, `get_plugin_categories`, `register_marketplace_plugin`

## Example Usage

### Prompt Management
```
Show me all available prompts with the tag "marketing"
```

```
Execute the "blog-article-generator" prompt with topic "AI in Sales"
```

### Project Management
```
List all projects in my workspace
```

```
Create a feature "User Authentication" in project TP
```

```
Generate development tasks from feature "Login System"
```

```
Update task TP-042 status to "in_progress"
```

### Quality Analysis
```
/quality-analysis
```

```
Show me quality trends for the last 30 days
```

### Test Analytics
```
Start a test session for homepage testing
```

```
Report a bug found during testing with screenshot
```

## Troubleshooting

### MCP Server Not Starting / Missing Environment Variables

If you see: `Missing environment variables: THINKPROMPT_API_URL, THINKPROMPT_API_KEY`

**Solution:** Add the `env` block to your `~/.claude/settings.json`:

```json
{
  "env": {
    "THINKPROMPT_API_URL": "https://thinkprompt-api-v2.azurewebsites.net/api/v1",
    "THINKPROMPT_API_KEY": "tp_your-api-key-here"
  }
}
```

Then restart Claude Code.

### Tools Not Available

Restart Claude Code after plugin installation or settings change.

### API Key Invalid

Get a fresh API key from https://thinkprompt.app/settings/api-keys and update the `env` block in `~/.claude/settings.json`

## Development

The plugin uses the ThinkPrompt MCP Server which runs via npx. No local MCP server installation required.

MCP Server repository: https://bitbucket.org/vernes_p/thinkprompt-mcp

## License

MIT

## Author

Honeyfield (dev@honeyfield.de)
https://thinkprompt.app
