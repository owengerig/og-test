#!/usr/bin/env python3
"""Writes last-run.md for og-test-workflow: one collapsible section per repository, and a header with the whole run's
result and duration. Run by og-test-one.yml's cleanup, once per repository, before it wipes the repository; each call
adds that repository's section to the sections already written in this run (a log from an earlier run is replaced).

Environment (set by og-test-one.yml): REPO, GITHUB_*, LABEL, INDEX, TOTAL, SOURCE_URL, SOURCE_REF, SOURCE_SHA, WF,
COPIED, BUNDLE_ID, BUILD_ID, IMPORT_RESULT, BUILD_RESULT, VERSION_FROM, VERSION_TO, VERSION_BACK, BUMP_VERSION_INPUT,
BUILD_INPUTS, REPO_LIST, PREV (the current last-run.md, if any), OUT (where to write it).
"""
import datetime as dt
import json
import os
import re
import subprocess

E = os.environ.get
REPO = E("REPO")
RUN_ID = E("GITHUB_RUN_ID")
RUN_URL = f"{E('GITHUB_SERVER_URL')}/{REPO}/actions/runs/{RUN_ID}"
LABEL = E("LABEL", "")
FENCE = "``````"   # logs can contain ``` themselves
RUN_MARK = f"<!-- og-test run {RUN_ID} -->"
SECTIONS_MARK = "<!-- og-test sections -->"
LOG_TAIL = 1500      # lines of the failed steps' log kept per repository (GitHub stops rendering very large files)


def gh(*args, default=""):
    try:
        return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=300).stdout
    except Exception:
        return default


def gh_json(path, default=None):
    out = gh("api", "--paginate", "--slurp", path)
    try:
        pages = json.loads(out)
        return pages
    except Exception:
        return default


def jobs(run_id):
    pages = gh_json(f"repos/{REPO}/actions/runs/{run_id}/jobs?per_page=100", []) or []
    return [j for p in pages for j in p.get("jobs", [])]


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def minutes(a, b):
    return max(0, round((b - a).total_seconds() / 60)) if a and b else None


def icon(result):
    return {"success": "✅", "failure": "❌", "cancelled": "⏹️", "skipped": "⏭️", "timed_out": "⌛"}.get(result or "", "⚠️")


def code(text):
    text = (text or "").rstrip()
    return f"{FENCE}text\n{text if text else '(nothing)'}\n{FENCE}\n"


def job_lines(js):
    out = []
    for j in js:
        res = j.get("conclusion") or j.get("status")
        took = minutes(ts(j.get("started_at")), ts(j.get("completed_at")))
        out.append(f"{icon(res)} {j['name']}: {res}" + (f" ({took} min)" if took is not None else ""))
        for s in j.get("steps") or []:
            sres = s.get("conclusion") or s.get("status")
            if sres not in ("success", "skipped"):
                out.append(f"     {icon(sres)} step: {s['name']}: {sres}")
    return "\n".join(out)


now = dt.datetime.now(dt.timezone.utc)
mine = [j for j in jobs(RUN_ID) if j["name"].startswith(LABEL + " /")]
repo_start = min((ts(j["started_at"]) for j in mine if j.get("started_at")), default=None)

import_res, build_res = E("IMPORT_RESULT"), E("BUILD_RESULT")
build_id = E("BUILD_ID", "")
build_jobs = jobs(build_id) if build_id else []
build_conclusion = ""
if build_id:
    build_conclusion = gh("run", "view", build_id, "-R", REPO, "--json", "conclusion", "--jq", ".conclusion").strip() or "unfinished"

ok = import_res == "success" and build_res == "success" and build_conclusion == "success"

# ---------- the one-line summary ----------
tag = gh("release", "list", "-R", REPO, "--limit", "1", "--json", "tagName", "--jq", ".[0].tagName").strip()
m = re.fullmatch(r"v?(.+?)-build(\d+)", tag)
built = f"version {m[1]} (build {m[2]})" if m else (f"version {E('VERSION_TO')}" if E("VERSION_TO") else "")
uploaded = any(re.search("testflight", s["name"], re.I) and s.get("conclusion") == "success"
               for j in build_jobs for s in (j.get("steps") or []))
took = minutes(repo_start, now)
took_txt = f" · {took} min" if took is not None else ""

if ok:
    what = f"succeeded, {built or 'version unknown'}" + (" uploaded to TestFlight" if uploaded else " (not uploaded to TestFlight)")
    if E("VERSION_TO"):
        what += f"; {E('VERSION_TO')} saved in the source repo" if E("VERSION_BACK") == "success" else f"; saving {E('VERSION_TO')} in the source repo: {E('VERSION_BACK') or 'not run'}"
else:
    where = ""
    for j in (build_jobs if build_id else mine):
        if j.get("conclusion") in ("failure", "cancelled", "timed_out"):
            step = next((s["name"] for s in (j.get("steps") or []) if s.get("conclusion") in ("failure", "cancelled", "timed_out")), "")
            where = f" at {j['name']}" + (f" › {step}" if step else "")
            break
    if import_res != "success":
        what = f"failed to import ({import_res})" + where
    elif not build_id:
        what = f"failed: Build iOS didn't start ({build_res})" + where
    else:
        what = f"failed ({build_conclusion}){where}" + (f", {built} was uploaded to TestFlight" if uploaded else "")

summary = f"{'✅' if ok else '❌'} <b>{LABEL}</b>: {what}{took_txt}"

# ---------- the details ----------
d = []
d.append("| | |\n|---|---|")
rows = [
    ("Result", f"{'✅ succeeded' if ok else '❌ failed'}"),
    ("Source", f"{E('SOURCE_URL')}{' (' + E('SOURCE_REF') + ')' if E('SOURCE_REF') else ''} at `{(E('SOURCE_SHA') or '?')[:12]}`"),
    ("Bundle ID", f"`{E('BUNDLE_ID') or '?'}`"),
    ("Built", built or "-"),
    ("Uploaded to TestFlight", "yes" if uploaded else "no"),
    ("Workflow run", f"`{E('WF') or '?'}` (copied: {E('COPIED') or '?'})"),
    ("Started with", f"`{E('BUILD_INPUTS', '')}`"),
    ("Bump version", f"{E('VERSION_FROM')} → {E('VERSION_TO')} (saved in the source repo: {E('VERSION_BACK') or 'not run'})"
                     if E("VERSION_TO") else ("on, but no version was set" if E("BUMP_VERSION_INPUT") == "true" else "off")),
    ("og-test-workflow jobs", f"import: {icon(import_res)} {import_res} · Build iOS: {icon(build_res)} {build_res}"),
    ("Build iOS run", f"{build_id} ({build_conclusion}; deleted by the cleanup)" if build_id else "not started"),
    ("Time", f"{repo_start:%Y-%m-%d %H:%M} → {now:%H:%M} UTC{took_txt}" if repo_start else "-"),
]
d += [f"| {k} | {v.replace('|', '/')} |" for k, v in rows]

d.append("\n**og-test-workflow jobs** (failed steps listed under their job)\n")
d.append(code(job_lines(mine)))

for j in mine:   # a failed og-test-workflow job (import, start / wait): its log
    if j.get("conclusion") == "failure":
        log = gh("api", f"repos/{REPO}/actions/jobs/{j['id']}/logs")
        d.append(f"\n**Log of {j['name']}** (last 300 lines)\n")
        d.append(code("\n".join(log.splitlines()[-300:])))

if build_id:
    d.append("\n**Build iOS jobs** (failed steps listed under their job)\n")
    d.append(code(job_lines(build_jobs)))
    notes = []
    for j in build_jobs:
        anns = gh("api", f"repos/{REPO}/check-runs/{j['id']}/annotations", "--jq",
                  '.[] | "\\(.annotation_level | ascii_upcase): \\(.message | gsub("\\n"; " "))"')
        notes += [a for a in anns.splitlines() if a and not re.search(r"node\.js 20", a, re.I)]
    d.append("\n**GitHub annotations**\n")
    d.append(code("\n".join(dict.fromkeys(notes))))
    if build_conclusion != "success":
        raw = gh("run", "view", build_id, "-R", REPO, "--log-failed")
        # "job<TAB>step<TAB>time line": keep step and line
        lines = []
        for line in raw.splitlines():
            parts = line.split("\t", 2)
            lines.append(f"[{parts[1]}] {parts[2]}" if len(parts) == 3 else line)
        lines = [l[:600] for l in lines]
        errs = [l for l in lines if re.search(r"##\[error\]|error CS\d+|[Ee]rror:|Exception|\*\* (ARCHIVE|EXPORT|BUILD) FAILED|exit code [1-9]|Build Finished, Result", l)]
        d.append(f"\n**Error lines from the failed steps** ({len(errs)})\n")
        d.append(code("\n".join(errs[-300:])))
        d.append(f"\n**Log of the failed steps** (last {min(LOG_TAIL, len(lines))} of {len(lines)} lines)\n")
        d.append(code("\n".join(lines[-LOG_TAIL:])))

section = (f"<!-- section result={'success' if ok else 'failure'} -->\n<details>\n<summary>{summary}</summary>\n\n"
           + "\n".join(d) + "\n</details>\n")

# ---------- this run's earlier sections ----------
prev = ""
if E("PREV") and os.path.exists(E("PREV")):
    prev = open(E("PREV"), encoding="utf-8", errors="replace").read()
sections = prev.split(SECTIONS_MARK, 1)[1].strip() + "\n\n" if RUN_MARK in prev and SECTIONS_MARK in prev else ""
sections += section

# ---------- header: the whole run ----------
results = re.findall(r"<!-- section result=(\w+) -->", sections)
total = int(E("TOTAL") or len(results))
failed = results.count("failure")
run_info = gh_json(f"repos/{REPO}/actions/runs/{RUN_ID}", [{}])[0] or {}
started = ts(run_info.get("run_started_at") or run_info.get("created_at"))
run_min = minutes(started, now)
done = len(results) >= total
if failed:
    head = f"❌ Failed: {failed} of {total} repositories failed" + ("" if done else f" (so far, {len(results)} of {total} done)")
elif done:
    head = f"✅ Succeeded: all {total} repositories"
else:
    head = f"⏳ In progress: {len(results)} of {total} done, all succeeded so far"

header = f"""{RUN_MARK}
# og-test last run: {head}

| | |
|---|---|
| Result | {head} |
| Duration | {run_min if run_min is not None else '?'} minutes{'' if done else ' so far'} |
| Run | [og-test-workflow #{E('GITHUB_RUN_NUMBER')}]({RUN_URL}), started {f'{started:%Y-%m-%d %H:%M} UTC' if started else '?'} |
| Repositories | {(E('REPO_LIST') or '').replace('|', '/')} |
| Bump version | {'on' if E('BUMP_VERSION_INPUT') == 'true' else 'off'} |

Each repository below: click to expand everything needed to troubleshoot it (its Build iOS run is deleted by the
cleanup). This file is replaced by every og-test-workflow run.

{SECTIONS_MARK}
"""
with open(E("OUT"), "w", encoding="utf-8") as f:
    f.write(header + "\n" + sections)
print(header)
print(summary)
