<!-- og-test run 45540190775 -->
# og-test last run: ✅ Succeeded: all 1 repositories

| | |
|---|---|
| Result | ✅ Succeeded: all 1 repositories |
| Duration | 23 minutes |
| Run | [og-test-workflow #13](https://github.com/owengerig/og-test/actions/runs/45540190775), started 2026-11-25 03:28 UTC |
| Repositories | ValleyOfDeath |
| Skipped | none |
| Version | build only |

Each repository below: click to expand everything needed to troubleshoot it (its Build iOS run is deleted by the
cleanup). This file is replaced by every og-test-workflow run.

<!-- og-test sections -->

<!-- section result=success -->
<details>
<summary>✅ <b>ValleyOfDeath (1 of 1)</b>: succeeded, version 0.1.2 (build 4) uploaded to TestFlight · 23 min</summary>

| | |
|---|---|
| Result | ✅ succeeded |
| Source | https://github.com/owengerig/ValleyOfDeath at `2c95a25f2f4b` |
| Bundle ID | `com.ogsoftware.valleyofdeath` |
| Built | version 0.1.2 (build 4) |
| Uploaded to TestFlight | yes |
| Workflow run | `build-ios.yml` (copied: build-ios.yml set-version.yml undo-version.yml) |
| Started with | `{"increment": "build only"}` |
| Version | build only |
| og-test-workflow jobs | import: ✅ success · Build iOS: ✅ success |
| Build iOS run | 45540246393 (success; deleted by the cleanup) |
| Time | 2026-11-25 03:28 → 03:51 UTC · 23 min |

**og-test-workflow jobs** (failed steps listed under their job)

``````text
✅ ValleyOfDeath (1 of 1) / Import repository: success (0 min)
✅ ValleyOfDeath (1 of 1) / Run its Build iOS: success (23 min)
⚠️ ValleyOfDeath (1 of 1) / Clean up og-test: in_progress
     ⚠️ step: Checkout og-test: in_progress
     ⚠️ step: Write last-run.md: pending
     ⚠️ step: Reset main to og-test's own files and last-run.md, without history: pending
     ⚠️ step: Delete other branches: pending
     ⚠️ step: Delete releases and tags: pending
     ⚠️ step: Delete artifacts and caches: pending
     ⚠️ step: Delete earlier workflow runs: pending
     ⚠️ step: Post Checkout og-test: pending
⏭️ ValleyOfDeath (1 of 1) / Save the new version in the source repository: skipped (0 min)
``````


**Build iOS jobs** (failed steps listed under their job)

``````text
✅ Set version / Set version: success (0 min)
✅ Check signing: success (0 min)
✅ Export Xcode project (Unity): success (8 min)
✅ Build with Xcode: success (13 min)
⏭️ Undo version: skipped (0 min)
``````


**GitHub annotations**

``````text
WARNING: Assets/Scripts/ValleyOfDeath/Game/Run.cs(22,32): warning UAC1001: Field 'character' type 'ValleyOfDeath.ValleyCharacter' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING: Assets/Scripts/ValleyOfDeath/Game/Combat.cs(135,26): warning UAC1001: Field 'def' type 'ValleyOfDeath.WeaponDef' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING: Assets/Scripts/ValleyOfDeath/Game/Player.cs(12,32): warning UAC1001: Field 'character' type 'ValleyOfDeath.ValleyCharacter' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING: Assets/Scripts/ValleyOfDeath/Game/Run.cs(24,41): warning UAC1001: Field 'Fists' type 'ValleyOfDeath.Item' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING: Assets/Scripts/ValleyOfDeath/Game/Run.cs(24,30): warning UAC1001: Field 'Secondary' type 'ValleyOfDeath.Item' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING: Assets/Scripts/ValleyOfDeath/Game/Run.cs(24,21): warning UAC1001: Field 'Primary' type 'ValleyOfDeath.Item' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING: Assets/Scripts/ValleyOfDeath/Game/Combat.cs(348,26): warning UAC1001: Field 'weapon' type 'ValleyOfDeath.WeaponDef' is skipped by serialization (missing the [Serializable] attribute). Refer to the Serialization rules analyzer reference. (https://docs.unity3d.com/6000.6/Documentation/Manual/script-serialization-analyzer.html#uac1001)
WARNING:        Library folder does not exist.       Consider setting up caching to speed up your workflow,       if this is not your first build.     
NOTICE: Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times.
``````

</details>
