# ad-claude-marketplace

Personal marketplace of Claude Code plugins — skills, utilities and (eventually) MCP
servers, independent of any single project or organisation.

## Install

```
/plugin marketplace add aadegtyarev/ad-claude-marketplace
/plugin install repo-docs@ad
```

## What ships

| Plugin | What's inside |
|---|---|
| **repo-docs** | `repo-docs` skill — write, rewrite and review the documentation that ships in a repository (`README.md`, `docs/`, guides). Splits pages by reader task (Diátaxis), strips machine-prose tells, adds Mermaid diagrams that show mechanism, and mechanically checks links/anchors/diagrams via `scripts/check_docs.py`. |

## Repo layout

```
ad-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── repo-docs/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/repo-docs/
            ├── SKILL.md
            ├── references/
            └── scripts/check_docs.py
```

## Adding a plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with `name`, `description`,
   `version` (start at `0.1.0`), `author`, `license`.
2. Register it in `.claude-plugin/marketplace.json`.
3. Bump `version` on every content change to that plugin — the marketplace only
   propagates an update to an already-installed plugin when its version string changes.

### Releasing a change — always bump the version

**Why this matters:** the marketplace only ships an *already-installed* plugin to a
user when its `plugin.json` `"version"` **changes**. Merging to `main` and running
`/plugin marketplace update` is not enough — Claude Code compares the cached version
against the marketplace one and skips the update when they match.

Bump `"version"` per SemVer 2.0:

- **patch** (`0.1.0 → 0.1.1`) — fix, wording, doc-only tweak.
- **minor** (`0.1.0 → 0.2.0`) — new skill, new capability, added reference.
- **major** (`0.1.0 → 1.0.0`) — breaking change to behaviour or contract.

**CI enforces this.** [`.github/workflows/plugin-version-check.yml`](.github/workflows/plugin-version-check.yml)
fails any PR that changes a plugin's content without bumping its version. Run the
same check locally before pushing:

```bash
python3 .github/scripts/check_plugin_versions.py     # diffs against origin/main
```

## License

MIT. See [LICENSE](LICENSE).
