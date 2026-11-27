#!/usr/bin/env python3
"""Points og-test's copied workflows at the private source repository, so the app's code never lands in og-test's git.

    og-test-source.py SOURCE_REPO BUILD_BRANCH FILE...

og-test is public. Its import commits only the copied workflow files (and the app's .github/scripts); the code is read
at build time, straight from the private source repository, with KIT_TOKEN. In every FILE (a copied workflow):

  1. every actions/checkout step gets   repository: SOURCE_REPO   and   token: ${{ secrets.KIT_TOKEN }}
  2. the branch Set version / Undo version check out and push to (github.ref_name / GITHUB_REF_NAME, og-test's own
     branch) becomes BUILD_BRANCH: a throwaway branch og-test makes in the source repository for this build and deletes
     in its cleanup, so the source's main only ever gets og-test's "Version x.y.z" commit after a successful build
  3. the steps that would publish the build in public og-test (Publish GitHub Release, Upload build artifact: the
     signed .ipa) are switched off (if: false). The .ipa still goes to TestFlight.

Exits 1 (and says why) if something can't be rewritten safely.
"""
import re
import sys

OFF_STEPS = {"Publish GitHub Release", "Upload build artifact"}


def indent(line):
    return len(line) - len(line.lstrip(" "))


def step_end(lines, start, step_indent):
    """Index after the last line of the step whose "- " is at lines[start] (dash at step_indent)."""
    i = start + 1
    while i < len(lines):
        s = lines[i]
        if s.strip() and not s.lstrip().startswith("#") and indent(s) <= step_indent:
            break
        i += 1
    return i


def rewrite(text, repo, branch, path):
    lines = text.split("\n")
    out, i, checkouts, offs = [], 0, 0, 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)(- )?uses: *actions/checkout@\S+", line)
        if m:
            # the step's keys are indented to where "uses" starts
            key_ind = len(m.group(1)) + (2 if m.group(2) else 0)
            dash_ind = key_ind - 2
            # the rest of the step: up to the next line at or left of its "- "
            end = step_end(lines, i, dash_ind)
            body = lines[i + 1:end]
            # drop any repository / token already in its with: block, then add ours
            body = [b for b in body if not re.match(r"^\s*(repository|token):", b)]
            w = next((k for k, b in enumerate(body) if re.match(r"^\s*with:\s*$", b) and indent(b) == key_ind), None)
            add = [" " * (key_ind + 2) + f"repository: {repo}   # og-test: the private source, read at build time",
                   " " * (key_ind + 2) + "token: ${{ secrets.KIT_TOKEN }}"]
            if w is None:
                body = [" " * key_ind + "with:"] + add + body
            else:
                body = body[:w + 1] + add + body[w + 1:]
            out.append(line)
            out.extend(body)
            checkouts += 1
            i = end
            continue
        m = re.match(r"^(\s*)- name: *[\"']?(.+?)[\"']?\s*$", line)
        if m and m.group(2) in OFF_STEPS:
            dash_ind = len(m.group(1))
            end = step_end(lines, i, dash_ind)
            body = [b for b in lines[i + 1:end] if not (re.match(r"^\s*if:", b) and indent(b) == dash_ind + 2)]
            out.append(line)
            out.append(" " * (dash_ind + 2) + "if: ${{ false }}   # og-test: nothing is published in public og-test")
            out.extend(body)
            offs += 1
            i = end
            continue
        out.append(line)
        i += 1
    text = "\n".join(out)
    text = text.replace("${{ github.ref_name }}", branch)
    text = re.sub(r"\$\{GITHUB_REF_NAME(:-[^}]*)?\}|\$GITHUB_REF_NAME\b", branch, text)
    return text, checkouts, offs


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    repo, branch, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    if not re.fullmatch(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+", repo) or not re.fullmatch(r"[A-Za-z0-9._/-]+", branch):
        print(f"::error::Bad source repository or branch: {repo} {branch}")
        return 1
    total = 0
    for path in files:
        with open(path) as f:
            text = f.read()
        new, n, offs = rewrite(text, repo, branch, path)
        # nothing may still check out or push og-test's own branch
        if re.search(r"github\.ref_name|GITHUB_REF_NAME", new):
            print(f"::error::{path} still uses og-test's branch name after the rewrite")
            return 1
        with open(path, "w") as f:
            f.write(new)
        total += n
        print(f"{path}: {n} checkout(s) now read {repo}" + (f", {offs} publishing step(s) off" if offs else ""))
    if total == 0:
        print("::error::None of the copied workflows checks out the code: nothing to point at the source repository")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
