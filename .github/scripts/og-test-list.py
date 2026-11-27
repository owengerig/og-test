#!/usr/bin/env python3
"""Works out og-test-workflow's list of repositories and prints it as JSON for the matrix.

REPOS    comma-separated names (nato-squad = github.com/<OWNER>/nato-squad), owner/name or links; name@branch for a
         branch. Empty = every repository the token (GH_TOKEN, the KIT_TOKEN) can see that has a "Build iOS" workflow;
         the others (og-utils, ...) are skipped and listed as such.
OWNER    the default owner for bare names.

Writes `repos` (the matrix JSON) and `skipped` (one line of what was left out and why) to GITHUB_OUTPUT.
"""
import json
import os
import re
import subprocess
import sys


def gh_api(path, raw=False):
    args = ["gh", "api", path] + (["-H", "Accept: application/vnd.github.raw"] if raw else [])
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def has_build_ios(full_name):
    """True if the repository has a startable (workflow_dispatch) workflow called "Build iOS" (or a build-ios.yml)."""
    listing = gh_api(f"repos/{full_name}/contents/.github/workflows")
    if not listing:
        return False
    files = [f["name"] for f in json.loads(listing) if f.get("type") == "file" and re.search(r"\.ya?ml$", f["name"])]
    # Only a Build iOS that can be started (workflow_dispatch) counts: og-workflows' shared unity-ios.yml is also
    # named "Build iOS" but is a reusable workflow (workflow_call only), not an app to build.
    for f in files:
        text = gh_api(f"repos/{full_name}/contents/.github/workflows/{f}", raw=True) or ""
        named = re.fullmatch(r"build-ios\.ya?ml", f, re.I) or re.search(r"""^name:\s*["']?Build iOS["']?\s*$""", text, re.M)
        if named and re.search(r"^\s*workflow_dispatch\s*:", text, re.M):
            return True
    return False


owner = os.environ["OWNER"]
given = [x.strip() for x in re.split(r"[,\n]", os.environ.get("REPOS", "")) if x.strip()]
skipped = []
entries = []   # (name, url, ref)

if given:
    for item in given:
        ref = ""
        if "@" in item.split("/")[-1]:   # name@branch or link@branch
            item, ref = item.rsplit("@", 1)
        item = item.rstrip("/")
        if re.fullmatch(r"[A-Za-z0-9._-]+", item):   # a bare name: one of our repos
            url = f"https://github.com/{owner}/{item}"
        elif re.fullmatch(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+", item):   # owner/name
            url = f"https://github.com/{item}"
        elif re.fullmatch(r"https://[A-Za-z0-9.-]+/\S+", item):
            url = item
        else:
            print(f"::error::\"{item}\" is not a repository name or https link", file=sys.stderr)
            sys.exit(1)
        name = re.sub(r"\.git$", "", url.rsplit("/", 1)[-1])
        entries.append((name, url, ref))
else:
    # every repository the token can see (a fine-grained token: the ones in its Repository access)
    raw = subprocess.run(["gh", "api", "--paginate", "--slurp", "user/repos?per_page=100"], capture_output=True, text=True)
    if raw.returncode != 0:
        print(f"::error::Couldn't list the KIT_TOKEN's repositories: {raw.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    repos = [r for page in json.loads(raw.stdout) for r in page]
    repos = sorted(repos, key=lambda r: r["name"].lower())
    for r in repos:
        name, full = r["name"], r["full_name"]
        if r.get("archived"):
            skipped.append(f"{name} (archived)")
        elif not has_build_ios(full):
            skipped.append(f"{name} (no Build iOS workflow)")
        else:
            entries.append((name, r["html_url"], ""))

if not entries:
    print("::error::Nothing to build" + (f" (skipped: {', '.join(skipped)})" if skipped else ""), file=sys.stderr)
    sys.exit(1)

total = len(entries)
matrix = [{"label": f"{name}{'@' + ref if ref else ''} ({i} of {total})", "url": url, "ref": ref, "total": str(total)}
          for i, (name, url, ref) in enumerate(entries, 1)]

with open(os.environ["GITHUB_OUTPUT"], "a") as o:
    o.write(f"repos={json.dumps(matrix)}\n")
    o.write(f"skipped={', '.join(skipped) or 'none'}\n")
    o.write(f"names={', '.join(n for n, _, _ in entries)}\n")

with open(os.environ.get("GITHUB_STEP_SUMMARY", os.devnull), "a") as s:
    s.write("### Repositories, in order\n")
    for m in matrix:
        s.write(f"- {m['label']}: {m['url']}{' (' + m['ref'] + ')' if m['ref'] else ''}\n")
    if skipped:
        s.write(f"\n**Skipped:** {', '.join(skipped)}\n")

for m in matrix:
    print(f"{m['label']}: {m['url']} {m['ref']}")
if skipped:
    print("Skipped: " + ", ".join(skipped))
