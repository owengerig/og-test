# og-test

A throwaway build bench: give it a link to one of the OG Software apps and it runs that app's own **Build iOS**
workflow here (signed `.ipa`, TestFlight upload), then wipes itself.

**Actions → og-test-workflow → Run workflow**, enter the repositories, comma-separated, and run:
`nato-squad, 2d-clash, CardCombat`. Each entry can be a name (one of owengerig's repos), `owner/name`, or a link;
add `@branch` to build a branch (`2d-clash@dev`).

They run **one at a time, in that order**, each through `og-test-one.yml`: import → its Build iOS → cleanup, then the
next one. A failed one doesn't stop the rest. At the end, `last-run.log` on `main` has a section for every repository
of the run.

| Step | What happens |
|---|---|
| Import | The repo is cloned and its files are committed onto `main` here, with its **Build iOS** workflow, the workflows that one calls (e.g. `set-version.yml`) and its `.github/scripts`. Its other workflows are left out. |
| Run its Build iOS | Started with: version = its default, *Increment the build number*, *app-store-connect*, *Upload to TestFlight*, *Build even if nothing changed*, and **Self Hosted off**. og-test-workflow waits for it to finish. |
| Clean up | Always runs, pass or fail: runs still going are cancelled, `main` goes back to one commit holding only og-test's `.github` and **`last-run.log`**, and every other branch, tag, release, artifact, cache and earlier workflow run is deleted. |

**GitHub's machines only.** og-test is public, so nothing runs on the laptop: Build iOS is started with Self Hosted
off, and the copied workflows' laptop labels (`og-linux`, `og-windows`, the `LINUX_RUNNER` / `WINDOWS_RUNNER`
variables) are swapped for GitHub's (`ubuntu-24.04`, `windows-latest`). The Xcode build is on GitHub's Mac as always.

**The source repo is never changed.** og-test-workflow only clones it (reads). Everything the copied workflows
write (version commit, release, tags) goes to og-test, and the import refuses to run copied workflows that name the
source repo directly.

Changes made to the copied workflows: the runner labels above, and `secrets.IOS_PROVISIONING_PROFILE_BASE64`
becomes `secrets.IOS_PROVISIONING_PROFILE_<APP>` (`<APP>` = the bundle ID's last part in capitals, e.g. `CLASH2D`,
`NATOSQUAD`), because og-test holds every app's profile.

Only `.github` and `last-run.log` live here permanently, which is why this README is in `.github/` (GitHub shows it on
the repo page).

## last-run.log

Written by each repository's cleanup, since its Build iOS run is deleted: one section per repository of the latest
og-test-workflow run (a new run replaces the whole file). Each section has:
the source repo, commit, bundle ID and the settings Build iOS was started with; every job and step of og-test-workflow
and of Build iOS with its result and times; GitHub's error annotations; and, when something failed, the error lines
and the last 20,000 lines of the failed steps' log (secrets show as `***`, as in GitHub's own logs).

## Setup

1. **Token:** add `og-test` to the KIT_TOKEN's Repository access (https://github.com/settings/personal-access-tokens),
   with Contents and Workflows: read and write.
2. **Secrets:** on the PC, run `push-github-secrets.ps1 -Only og-test` (og-utils). It pushes KIT_TOKEN, the Unity
   login and licence, the iOS certificate, the Team ID (as both `IOS_TEAM_ID` and `APPLE_TEAM_ID`), the App Store
   Connect key, and every app's App Store profile as `IOS_PROVISIONING_PROFILE_<APP>`.
3. **Visibility:** this repo should be **private**: while a run is going, the app's source and the `.ipa` sit here.

## Notes

- The version bump is only saved in the throwaway copy, not in the app's own repo. The copied set-version step
  still raises the build number above whatever TestFlight already has.
- PinTally's Firebase files and StoryHub's own secrets aren't pushed to og-test, so those two build here without them.
- On GitHub's machines Unity imports the whole project every time (no saved Library), so a build takes longer than
  on the laptop.
- GitHub can't delete a run while it's running, so the latest og-test-workflow run stays in the Actions list until
  the next one.
