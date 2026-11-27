<!-- og-test run 46050175593 -->
# og-test last run: ✅ Succeeded: all 2 repositories

| | |
|---|---|
| Result | ✅ Succeeded: all 2 repositories |
| Duration | 60 minutes |
| Run | [og-test-workflow #15](https://github.com/owengerig/og-test/actions/runs/46050175593), started 2026-11-27 18:31 UTC |
| Repositories | 2d-clash, nato-squad |
| Skipped | none |
| Version | skip |

Each repository below: click to expand everything needed to troubleshoot it (its Build iOS run is deleted by the
cleanup). This file is replaced by every og-test-workflow run.

<!-- og-test sections -->

<!-- section result=success -->
<details>
<summary>✅ <b>2d-clash (1 of 2)</b>: succeeded, version unknown uploaded to TestFlight · 28 min</summary>

| | |
|---|---|
| Result | ✅ succeeded |
| Source | https://github.com/owengerig/2d-clash at `b0eec7954495` |
| Bundle ID | `com.ogsoftware.clash2d` |
| Built | - |
| Uploaded to TestFlight | yes |
| Workflow run | `build-ios.yml` (copied: build-ios.yml unity-ios.yml set-version.yml undo-version.yml) |
| Started with | `{"increment": "skip"}` |
| Version | skip |
| og-test-workflow jobs | import: ✅ success · Build iOS: ✅ success |
| Build iOS run | 46050231025 (success; deleted by the cleanup) |
| Time | 2026-11-27 18:32 → 18:59 UTC · 28 min |

**og-test-workflow jobs** (failed steps listed under their job)

``````text
✅ 2d-clash (1 of 2) / Import repository: success (0 min)
✅ 2d-clash (1 of 2) / Run its Build iOS: success (27 min)
⚠️ 2d-clash (1 of 2) / Clean up og-test: in_progress
     ⚠️ step: Checkout og-test: in_progress
     ⚠️ step: Write last-run.md: pending
     ⚠️ step: Reset main to og-test's own files and last-run.md, without history: pending
     ⚠️ step: Delete other branches: pending
     ⚠️ step: Delete releases and tags: pending
     ⚠️ step: Delete artifacts and caches: pending
     ⚠️ step: Delete earlier workflow runs: pending
     ⚠️ step: Post Checkout og-test: pending
⏭️ 2d-clash (1 of 2) / Save the new version in the source repository: skipped (0 min)
``````


**Build iOS jobs** (failed steps listed under their job)

``````text
✅ iOS / Set version / Set version: success (0 min)
✅ iOS / Check signing: success (0 min)
✅ iOS / Export Xcode project (Unity): success (12 min)
✅ iOS / Build with Xcode: success (15 min)
⏭️ iOS / Undo version: skipped (0 min)
``````


**GitHub annotations**

``````text
WARNING: [ServicesCore]: To use Unity's dashboard services, you need to link your Unity project to a project ID. To do this, go to Project Settings to select your organization, select your project and then link a project ID. You also need to make sure your organization has access to the required products. Visit https://dashboard.unity3d.com to sign up.
WARNING: [2D Clash] build numbers differ (game shows 3, Android 15, iOS 15); use 2D Clash → Version → Bump Build Only to line them up.
WARNING:        Library folder does not exist.       Consider setting up caching to speed up your workflow,       if this is not your first build.
``````

</details>

<!-- section result=success -->
<details>
<summary>✅ <b>nato-squad (2 of 2)</b>: succeeded, version unknown uploaded to TestFlight · 32 min</summary>

| | |
|---|---|
| Result | ✅ succeeded |
| Source | https://github.com/owengerig/nato-squad at `dcc340779b54` |
| Bundle ID | `com.ogsoftware.natosquad` |
| Built | - |
| Uploaded to TestFlight | yes |
| Workflow run | `build-ios.yml` (copied: build-ios.yml unity-ios.yml set-version.yml undo-version.yml) |
| Started with | `{"increment": "skip"}` |
| Version | skip |
| og-test-workflow jobs | import: ✅ success · Build iOS: ✅ success |
| Build iOS run | 46053560941 (success; deleted by the cleanup) |
| Time | 2026-11-27 19:00 → 19:32 UTC · 32 min |

**og-test-workflow jobs** (failed steps listed under their job)

``````text
✅ nato-squad (2 of 2) / Import repository: success (0 min)
✅ nato-squad (2 of 2) / Run its Build iOS: success (32 min)
⚠️ nato-squad (2 of 2) / Clean up og-test: in_progress
     ⚠️ step: Checkout og-test: in_progress
     ⚠️ step: Write last-run.md: pending
     ⚠️ step: Reset main to og-test's own files and last-run.md, without history: pending
     ⚠️ step: Delete other branches: pending
     ⚠️ step: Delete releases and tags: pending
     ⚠️ step: Delete artifacts and caches: pending
     ⚠️ step: Delete earlier workflow runs: pending
     ⚠️ step: Post Checkout og-test: pending
⏭️ nato-squad (2 of 2) / Save the new version in the source repository: skipped (0 min)
``````


**Build iOS jobs** (failed steps listed under their job)

``````text
✅ iOS / Set version / Set version: success (0 min)
✅ iOS / Check signing: success (0 min)
✅ iOS / Export Xcode project (Unity): success (14 min)
✅ iOS / Build with Xcode: success (16 min)
⏭️ iOS / Undo version: skipped (0 min)
``````


**GitHub annotations**

``````text
WARNING: [NATO Squad] build numbers differ (game shows 2, Android 12, iOS 12); use NATO Squad → Version → Bump Build Only to line them up.
WARNING: [ServicesCore]: To use Unity's dashboard services, you need to link your Unity project to a project ID. To do this, go to Project Settings to select your organization, select your project and then link a project ID. You also need to make sure your organization has access to the required products. Visit https://dashboard.unity3d.com to sign up.
WARNING:        Library folder does not exist.       Consider setting up caching to speed up your workflow,       if this is not your first build.
``````

</details>
