# og-test

A throwaway build bench: give it a link to one of the OG Software apps and it runs that app's own **Build iOS**
workflow here (signed `.ipa`, TestFlight upload), then wipes itself.

**Actions → og-test-workflow → Run workflow**:

- **Repos:** comma-separated, e.g. `nato-squad, 2d-clash, CardCombat`. Each can be a name (one of owengerig's repos),
  `owner/name` or a link; add `@branch` to build a branch (`2d-clash@dev`). **Leave it empty to build every repo the
  KIT_TOKEN can see** that has a Build iOS workflow; the rest (og-utils, og-content, ...) are skipped and listed as
  skipped in the run summary and `last-run.md`.

**Version** is passed to each repository's Build iOS: **build only** (the default: just +1 build), **patch** (1.3.0 →
1.3.1), **minor** (→ 1.4.0), **major** (→ 2.0.0) or **skip**. With patch, minor or major, when that repository's Build
iOS succeeds, the new version is committed to the source repository (only the version: the same files set-version.sh
writes it to). If the build fails, the source keeps its old version.

They run **one at a time, in that order**, each through `og-test-one.yml`: import → its Build iOS → cleanup, then the
next one. A failed one doesn't stop the rest. At the end, `last-run.md` on `main` has a section for every repository
of the run.

| Step | What happens |
|---|---|
| Import | Only the repo's **Build iOS** workflow is committed onto `main` here (never the app's code: see *The app's code stays private* below), with the workflows that one calls (e.g. `set-version.yml`) and its `.github/scripts`. When the app's Build iOS uses the shared build steps in [og-workflows](https://github.com/owengerig/og-workflows) (private, so og-test can't call them), the shared workflows it calls are copied from there too and called as local copies; this needs og-workflows in `KIT_TOKEN`'s repository access. Its other workflows are left out. Files a previous run left in `.github` (anything but og-test's own) are removed first. |
| Run its Build iOS | Started with the chosen **Version** (default **build only**); Build iOS always builds on GitHub's machines and uploads to TestFlight. og-test-workflow waits for it to finish. |
| Clean up | Always runs, pass or fail: runs of the copied workflows still going are cancelled (og-test-workflow runs waiting in the queue are left alone and start next), `main` goes back to one commit holding only og-test's `.github` and **`last-run.md`**, and every other branch, tag, release, artifact, cache and finished workflow run is deleted. The reset of `main` is retried up to 5 times (GitHub once answered it with a 500). |

**GitHub's machines only.** og-test is public, so nothing runs on the laptop: Build iOS is started with Self Hosted
off, and the copied workflows' laptop labels (`og-linux`, `og-windows`, the `LINUX_RUNNER` / `WINDOWS_RUNNER`
variables) are swapped for GitHub's (`ubuntu-24.04`, `windows-latest`). The Xcode build is on GitHub's Mac as always.

**The app's code stays private.** og-test is public, so the app's code is never committed here (until Nov 26, 2026
every import put the whole app on public `main` for the length of its build). The copied workflows check the code out
straight from the private source repo at build time, with KIT_TOKEN (`.github/scripts/og-test-source.py` adds
`repository:` and `token:` to every `actions/checkout` step), so it only ever exists on GitHub's build machine. The
import refuses to commit anything outside `.github`.

**The source repo's branches are never changed**, except for the version commit after a successful patch / minor /
major build. The copied Set version and Undo version commit the new numbers to a throwaway branch in the source repo,
**`og-test-build`**, which the import makes at the commit being built and cleanup deletes (if a run is cut short, it
may be left behind: delete it by hand). The import refuses to run copied workflows that name the source repo
directly.

Changes made to the copied workflows: the runner labels above; `secrets.IOS_PROVISIONING_PROFILE_BASE64`
becomes `secrets.IOS_PROVISIONING_PROFILE_<APP>` (`<APP>` = the bundle ID's last part in capitals, e.g. `CLASH2D`,
`NATOSQUAD`), because og-test holds every app's profile; every checkout reads the source repo and Set version / Undo
version use `og-test-build` (above); and **Publish GitHub Release** and **Upload build artifact** (the signed `.ipa`)
are switched off, so nothing from the build is published here. The `.ipa` still goes to TestFlight.

**What's still visible while a build runs:** the run's logs, and the Unity games' intermediate Xcode-project artifact
(passed from the Unity job to the Xcode job). Both are deleted by cleanup, minutes later.

Only `.github` and `last-run.md` live here permanently, which is why this README is in `.github/` (GitHub shows it on
the repo page).

## last-run.md

Written by each repository's cleanup, since its Build iOS run is deleted (a new og-test-workflow run replaces the file).

- **At the top:** whether the whole run succeeded or failed (how many repositories failed) and how long it took, in minutes.
- **One collapsible section per repository:** its one-line summary says whether it succeeded or failed (and where), the
  version and build it built, whether it went to TestFlight, and whether the new version (patch / minor / major) was saved in the
  source repo. Expand it for everything needed to troubleshoot: source commit, bundle ID, settings, every job and
  failed step with times, GitHub's annotations, the error lines, and the last 1,500 lines of the failed steps' log
  (secrets show as `***`).

## Setup

1. **Token:** add `og-test` to the KIT_TOKEN's Repository access (https://github.com/settings/personal-access-tokens),
   with Contents and Workflows: read and write.
2. **Secrets:** on the PC, run `push-github-secrets.ps1 -Only og-test` (og-utils). It pushes KIT_TOKEN, the Unity
   login and licence, the iOS certificate, the Team ID (as both `IOS_TEAM_ID` and `APPLE_TEAM_ID`), the App Store
   Connect key, and every app's App Store profile as `IOS_PROVISIONING_PROFILE_<APP>`.
3. **Visibility:** this repo stays **public** (free macOS minutes). The app's code is never committed here (above).
4. **Token, source repos:** KIT_TOKEN needs **Contents: Read and write** on each app repo (to read the code and make
   and delete `og-test-build`).

## Notes

- Build numbers are only saved on the throwaway `og-test-build` branch, not on the app's main branch. The copied set-version step
  still raises the build number above whatever TestFlight already has.
- PinTally's Firebase files and StoryHub's own secrets aren't pushed to og-test, so those two build here without them.
- On GitHub's machines Unity imports the whole project every time (no saved Library), so a build takes longer than
  on the laptop.
- GitHub can't delete a run while it's running, so the latest og-test-workflow run stays in the Actions list until
  the next one.

## TODO

- [ ] **First run with the code read at build time.** Start og-test-workflow with Repos `PinTally` (the quickest
  build) and Version **build only**; check that it reaches TestFlight, that `main` here only ever holds `.github` and
  `last-run.md`, and that `og-test-build` is gone from PinTally afterwards. Then a Unity game (e.g. `2d-clash`).
- [ ] **Ask GitHub Support to purge og-test's old commits.** Every import before Nov 26, 2026 committed an app's
  whole code here; cleanup force-pushed it away, but GitHub keeps unreachable commits viewable by their SHA until it
  garbage-collects them. Support (https://support.github.com, "Remove sensitive data") can purge them and their
  cached views.
- [ ] **Encrypt the Unity games' Xcode-project artifact (optional).** It's the one piece of a build still
  downloadable here while the build runs (deleted by cleanup minutes later).
