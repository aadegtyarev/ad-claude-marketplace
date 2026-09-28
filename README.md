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

## License

MIT. See [LICENSE](LICENSE).
