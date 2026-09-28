#!/usr/bin/env python3
"""Fail when a marketplace plugin's content changed but its version wasn't bumped.

Why this exists
---------------
Claude Code (and Copilot CLI) propagate an *already-installed* plugin to users
only when the ``version`` field in its ``.claude-plugin/plugin.json`` changes.
A plain git push to the marketplace repo does nothing on its own: on
``/plugin marketplace update`` the client compares the resolved version against
its cached copy and skips the update when they match. So a PR that edits a
skill but forgets to bump the plugin version ships nothing — the new skill
silently never reaches anyone who already had the plugin.

This check catches that class of bug in CI: for every local plugin listed in
``.claude-plugin/marketplace.json``, if any file under the plugin directory
changed in this PR, the plugin's ``version`` must differ from the base branch.

Usage
-----
    # CI (GitHub Actions sets BASE_SHA to the PR base commit)
    BASE_SHA=<sha> python3 .github/scripts/check_plugin_versions.py

    # Locally, before pushing — defaults the base to origin/main
    python3 .github/scripts/check_plugin_versions.py

Exit code 0 = all good, 1 = at least one plugin needs a version bump (or a
structural problem), 2 = the check itself could not run.

No third-party dependencies — standard library only.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN_MANIFEST = Path(".claude-plugin") / "plugin.json"

# ANSI colours, but only when stdout is a TTY (GitHub Actions logs render them).
_TTY = sys.stdout.isatty() or os.environ.get("GITHUB_ACTIONS") == "true"
RED = "\033[31m" if _TTY else ""
GREEN = "\033[32m" if _TTY else ""
YELLOW = "\033[33m" if _TTY else ""
BOLD = "\033[1m" if _TTY else ""
RESET = "\033[0m" if _TTY else ""


def git(*args: str) -> str:
    """Run a git command from the repo root and return stripped stdout."""
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def fail_hard(message: str) -> None:
    """Print an error and exit 2 — the check itself could not run."""
    print(f"{RED}{BOLD}check-plugin-versions: {message}{RESET}", file=sys.stderr)
    sys.exit(2)


def resolve_base() -> str:
    """Resolve the commit to diff against: the merge-base of BASE_SHA (or
    origin/main) with HEAD, so we only look at what this branch introduced."""
    base_ref = os.environ.get("BASE_SHA") or "origin/main"
    try:
        return git("merge-base", base_ref, "HEAD")
    except subprocess.CalledProcessError:
        # Shallow checkout or unknown ref — fall back to the ref itself.
        try:
            return git("rev-parse", base_ref)
        except subprocess.CalledProcessError:
            fail_hard(
                f"cannot resolve base ref {base_ref!r}. "
                "In CI, set BASE_SHA and fetch it (actions/checkout fetch-depth: 0)."
            )
    return ""  # unreachable, keeps type-checkers happy


def local_plugins() -> list[tuple[str, str]]:
    """Return (name, relative_dir) for every plugin in marketplace.json whose
    source is a local path. Cross-repo plugins (object source) are skipped —
    their versions are enforced in their own repo."""
    try:
        data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail_hard(f"cannot read {MARKETPLACE.relative_to(REPO_ROOT)}: {exc}")
    plugins = []
    for entry in data.get("plugins", []):
        source = entry.get("source")
        if isinstance(source, str):  # local path like "./plugins/repo-docs"
            plugins.append((entry.get("name", source), source.lstrip("./")))
    return plugins


def version_at(ref: str, manifest_rel: str) -> str | None:
    """Read the "version" field of a plugin.json at a given git ref.
    Returns None if the file did not exist at that ref (a brand-new plugin)."""
    try:
        blob = git("show", f"{ref}:{manifest_rel}")
    except subprocess.CalledProcessError:
        return None  # file absent at base → new plugin
    try:
        return json.loads(blob).get("version")
    except json.JSONDecodeError:
        return None


def version_in_tree(manifest_path: Path) -> str | None:
    """Read the "version" field from the working-tree plugin.json (== HEAD in
    CI; includes uncommitted edits locally, which is what a dev wants)."""
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8")).get("version")
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    base = resolve_base()
    print(f"{BOLD}Checking plugin version bumps against {base[:12]}{RESET}\n")

    failures: list[str] = []

    for name, rel_dir in local_plugins():
        manifest_rel = f"{rel_dir}/{PLUGIN_MANIFEST.as_posix()}"
        manifest_path = REPO_ROOT / manifest_rel

        # Files changed under this plugin between base and the working tree,
        # ignoring the manifest itself (the bump lives there).
        changed = [
            line
            for line in git("diff", "--name-only", base, "--", rel_dir).splitlines()
            if line and not line.endswith(PLUGIN_MANIFEST.as_posix())
        ]
        if not changed:
            print(f"  {GREEN}·{RESET} {name}: no content change")
            continue

        head_version = version_in_tree(manifest_path)
        if head_version is None:
            failures.append(
                f"{name}: ships via marketplace and changed in this PR, but "
                f'{manifest_rel} is missing or has no "version" field.'
            )
            print(f"  {RED}✗{RESET} {name}: no version field ({len(changed)} file(s) changed)")
            continue

        base_version = version_at(base, manifest_rel)
        if base_version is None:
            # New plugin — nothing cached on users' machines yet, no bump needed.
            print(f"  {GREEN}+{RESET} {name}: new plugin at v{head_version}")
            continue

        if base_version == head_version:
            failures.append(
                f"{name}: {len(changed)} file(s) changed but version is still "
                f"{base_version}. Existing installs will NOT receive the update.\n"
                f'      Bump "version" in {manifest_rel} (SemVer: patch=fix/doc, '
                f"minor=new content, major=breaking).\n"
                f"      First changed file: {changed[0]}"
            )
            print(
                f"  {RED}✗{RESET} {name}: changed but version still {base_version} "
                f"({len(changed)} file(s))"
            )
        else:
            print(
                f"  {GREEN}✓{RESET} {name}: {base_version} → {head_version} "
                f"({len(changed)} file(s) changed)"
            )

    print()
    if failures:
        print(
            f"{RED}{BOLD}Version-bump check FAILED — {len(failures)} plugin(s) "
            f"need a version bump:{RESET}\n"
        )
        for f in failures:
            print(f"  {RED}✗{RESET} {f}\n")
        print(
            f"{YELLOW}Why this matters:{RESET} the marketplace only propagates an "
            'already-installed plugin when its plugin.json "version" changes. '
            "Without a bump, your merged change reaches nobody who already has the "
            'plugin. See README → "Releasing a change".'
        )
        return 1

    print(f"{GREEN}{BOLD}All changed plugins have a version bump.{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
