# MangroveTrader Plugin -- Marketplace Submission Plan

Prepare the plugin for submission to the official Claude Code plugin directory.

## Step 1: Rename GitHub Repo

Rename `mangrove-trader-plugin` -> `mangrove-trader-plugin` (singular).

**How:** GitHub Settings > General > Repository name > Rename. GitHub auto-redirects the old URL.

**Impact:** Every reference to the repo URL needs updating across both repos.

### References to update in mangrove-trader-plugin (this repo):

| File | What to change |
|------|----------------|
| `.claude-plugin/plugin.json` | `repository` URL |
| `.claude-plugin/marketplace.json` | `name` field |
| `README.md` | clone URL, marketplace add command, plugin-dir path |
| `CLAUDE.md` | Any repo name references |
| `docs/user-guide.md` | clone URL, marketplace add, plugin-dir |
| `docs/plans/mt-command-parity.md` | repo name references |

### References to update in MangroveTrader:

| File | What to change |
|------|----------------|
| `site/src/components/Nav.astro` | 2 GitHub links |
| `site/src/components/Footer.astro` | GitHub link |
| `site/src/components/Hero.astro` | GitHub link |
| `site/src/pages/docs/plugins.astro` | clone URL, marketplace add, plugin-dir, architecture tree, repo link |
| `site/src/pages/docs/index.astro` | GitHub link |
| `site/src/layouts/Docs.astro` | GitHub link |
| `docs/endpoints.md` | Plugin reference |
| `docs/user-stories.md` | Plugin reference |
| `docs/reports/2026-03-22-payment-surface-audit.md` | Plugin repo URL |

### References to update in portfolio:

| File | What to change |
|------|----------------|
| `memory/MEMORY.md` | Repo name in active list, memory path |
| `memory/repos/mangrove-trader-plugin/REPO_MEMORY.md` | Rename directory? Or leave as-is (memory is internal) |
| `CLAUDE.md` (portfolio root) | Project table |
| `.mcp.json` (portfolio root) | No change needed (URL is api.mangrovetraders.com, not repo) |

## Step 2: Apply Community Lessons

Based on research of published plugins and community feedback:

### 2a. Structure verification

- [x] `plugin.json` is in `.claude-plugin/` (correct)
- [x] `commands/`, `skills/`, `hooks/` are at plugin root (correct -- common mistake is nesting inside .claude-plugin/)
- [x] `marketplace.json` is in `.claude-plugin/` (correct)
- [ ] `marketplace.json` version should match `plugin.json` version (currently 1.0.0 vs 2.0.0 -- fix)

### 2b. plugin.json improvements

- [ ] Add `homepage` field: `"homepage": "https://mangrovetraders.com"`
- [ ] Add `license` field: `"license": "MIT"`
- [ ] Add `category` field: `"category": "productivity"` (matches marketplace.json)
- [ ] Verify `keywords` are discoverable terms people would search for

### 2c. README improvements

- [ ] Add link to MangroveTrader website at the top
- [ ] Add link to the MangroveTrader Twitter account
- [ ] Add "What is MangroveTrader?" section before Install (don't assume reader knows)
- [ ] Add badges (optional but common in published plugins)
- [ ] Add screenshot or example output (if practical)

### 2d. Transparency for MCP server review

Since our plugin connects to a remote MCP server, reviewers will want to know:
- [ ] What data the MCP server accesses (trading data, no PII)
- [ ] What the payment flow does (x402 micropayments, user must confirm)
- [ ] That no credentials are stored or transmitted by the plugin
- [ ] That the MCP server source code is public (MangroveTrader repo)

Add a "Security & Privacy" section to README covering these points.

### 2e. Code vs Claude boundary (Pierce Lamb lesson)

Review SKILL.md to ensure:
- [ ] Instructions that can be explicit (tool params, error handling) ARE explicit
- [ ] LLM judgment is only used where needed (interpreting user intent, presenting results)
- [ ] No vague "figure it out" instructions

## Step 3: Submit

1. Verify all changes are committed and pushed
2. Go to `claude.ai/settings/plugins/submit` or `platform.claude.com/plugins/submit`
3. Submit the plugin with:
   - Repository URL: `https://github.com/MangroveTechnologies/mangrove-trader-plugin`
   - Plugin name: `mangrove-trader`
   - Category: productivity
4. Wait for automated review
5. If accepted, users can install with: `claude plugin install mangrove-trader`

## Step 4: Also Submit to Community Directories

- [claudemarketplaces.com](https://claudemarketplaces.com/) -- community directory
- [claude-plugins.dev](https://claude-plugins.dev/) -- community registry
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) -- curated list (submit PR)

## Execution Order

1. Rename the GitHub repo first (all URL updates depend on this)
2. Update all references in both repos (one PR each)
3. Apply plugin.json and README improvements (same PR as #2 in plugin repo)
4. Submit to Anthropic
5. Submit to community directories
