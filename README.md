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

### Install from Marketplace

**Step 1:** Add the ThinkPrompt marketplace:
```bash
/plugin marketplace add https://thinkprompt-api-v2.azurewebsites.net/api/v1/plugins/marketplace.json
```

**Step 2:** Install the plugin:
```bash
/plugin install thinkprompt
```

Or use the interactive plugin manager:
```bash
/plugin
```
Then navigate to **Discover** tab and select ThinkPrompt.

### Alternative: Install from GitHub

```bash
# 1. Add the GitHub marketplace
/plugin marketplace add Honeyfield-Org/thinkprompt-plugin

# 2. Install the plugin
/plugin install thinkprompt
```

### Configure API Key

You have two options to configure your API key:

#### Option 1: Setup Command (Recommended)

Run the setup command in Claude Code:

```
/setup-thinkprompt
```

Claude will:
1. Ask for your API key
2. Save it to `~/.claude/settings.json`
3. Tell you to restart Claude Code

**Get your API key from:** https://thinkprompt.ai/settings

#### Option 2: Manual Configuration

Add the environment variables to your Claude Code settings file `~/.claude/settings.json`:

```json
{
  "env": {
    "THINKPROMPT_API_URL": "https://thinkprompt-api-v2.azurewebsites.net/api/v1",
    "THINKPROMPT_API_KEY": "tp_your-api-key-here"
  }
}
```

**Get your API key from:** https://thinkprompt.ai/settings
**Note:** Claude Code resolves `${VAR}` references in `.mcp.json` from the `env` block in `settings.json`. You don't need to create a separate `.env` file.

#### For Local Development

```json
{
  "env": {
    "THINKPROMPT_API_URL": "http://localhost:3001/api/v1",
    "THINKPROMPT_API_KEY": "tp_your-api-key-here"
  }
}
```

### Claude Desktop Integration

You can also use ThinkPrompt in Claude Desktop. Add this to your config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "thinkprompt": {
      "command": "npx",
      "args": ["@honeyfield/thinkprompt-mcp"],
      "env": {
        "THINKPROMPT_API_URL": "https://thinkprompt-api-v2.azurewebsites.net/api/v1",
        "THINKPROMPT_API_KEY": "tp_your-api-key-here"
      }
    }
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

### `/setup-thinkprompt`

Configure your ThinkPrompt API credentials interactively.

```bash
/setup-thinkprompt
```

Claude will ask for your API key and save it to `~/.claude/settings.json`. After setup, restart Claude Code.

### `/setup-workspace`

Set up ThinkPrompt for your project. Analyzes codebase, creates project, style guides, and useful prompts.

```bash
/setup-workspace
```

Claude will:
1. **Analyze your codebase** - Detect frameworks, languages, and tools (Next.js, NestJS, Angular, etc.)
2. **Create a ThinkPrompt project** - With name, slug, and description based on detected stack
3. **Set up style guides** - Load existing template or generate based on code analysis
4. **Create useful prompts** - Code Review, Feature Planning, Bug Report, Commit Message

Best run once when starting a new project to get the full ThinkPrompt integration.

### `/feature-dev-tp`

Feature development with automatic style guide loading from ThinkPrompt.

```bash
/feature-dev-tp <feature-description>
```

Automatically detects your project type and loads the appropriate style guide before implementing the feature. Supports Next.js, NestJS, Angular, Vue, Nuxt, Svelte, Remix, Astro, React Native/Expo, Python (Django, FastAPI, Flask), Rust, Go, Java/Kotlin, PHP, and Ruby. When multiple style guides match, you can choose which one to use.

### `/prompts`

List, search, execute, and create ThinkPrompt prompts.

```bash
# Show all prompts
/prompts

# Search and execute a prompt
/prompts code review

# Create a new prompt
/prompts new
```

Claude will:
1. **List your prompts** - With variables count and descriptions
2. **Execute prompts** - Fill in variables interactively
3. **Create prompts** - Guided creation with templates for analysis, generation, planning

### `/templates`

Browse and apply ThinkPrompt templates (Style Guides and Example Prompts).

```bash
# Show all templates
/templates

# Filter by type
/templates styles
/templates examples

# Search by framework
/templates nextjs

# Create new template
/templates new
```

Claude will:
1. **Browse templates** - Style Guides and Example Prompts
2. **Apply Style Guides** - View and use for your project
3. **Convert to prompts** - Turn Example Prompts into usable prompts
4. **Create templates** - Generate Style Guides from code analysis

### `/tasks`

View and manage ThinkPrompt tasks for your project.

```bash
# Show all tasks
/tasks

# Filter by status
/tasks open
/tasks wip
/tasks blocked
/tasks done

# View specific task
/tasks TP-042

# Search tasks
/tasks authentication
```

Claude will:
1. **Auto-detect your project** - Match current directory to ThinkPrompt project
2. **Show task overview** - Grouped by status with priorities
3. **Allow status updates** - Change task status directly
4. **Show task details** - Full info including comments and history

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

## Agents

The plugin includes specialized AI agents that trigger automatically based on context:

### Feature Task Planner
Helps break down features into development tasks. Triggers when you say things like:
- "I need to implement user notifications, help me plan the tasks"
- "Break down this feature into development tasks"

### Code Reviewer
Reviews code for architecture, security, and best practices. Automatically loads matching style guides from ThinkPrompt based on your project type. Triggers when:
- You complete implementing a feature
- You ask for a code review

### Quality Analysis Agent
Runs comprehensive code quality checks. Triggers when you ask:
- "Run a quality check on the codebase"
- "How is the code quality looking?"

## Skills

Contextual guides that are loaded automatically when relevant:

### Prompt Engineering
Best practices for creating effective prompts in ThinkPrompt. Loaded when:
- Creating new prompts or templates
- Asking about prompt best practices
- Working with ThinkPrompt variables

### Feature Workflow
End-to-end feature development workflow guide. Loaded when:
- Starting a new feature
- Asking about the development process
- Planning larger implementations

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

**Solution:** Run the setup command:

```
/setup-thinkprompt
```

Or manually add the `env` block to your `~/.claude/settings.json`:

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

Get a fresh API key from https://thinkprompt.ai/settings and run `/setup-thinkprompt` again, or manually update the `env` block in `~/.claude/settings.json`.

## Development

The plugin uses the ThinkPrompt MCP Server which runs via npx. No local MCP server installation required.

MCP Server repository: https://bitbucket.org/vernes_p/thinkprompt-mcp

## License

MIT

## Author

Honeyfield (dev@honeyfield.de)
https://thinkprompt.ai
