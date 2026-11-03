---
name: brew-update
description: Update a Brew page or shared Brew behavior locally, verify it, then commit and push to Brian's owning personal repositories. Meaningful reusable Brew changes also require a PR into the Kubera app. Use for Brew maintenance, not automatic hosted publication.
---

# Update Brew

Invoke with `/skill:brew-update <page, behavior, or change>`. A concrete invocation authorizes the
scoped local update, verification, personal-repo commits/pushes and, for meaningful reusable changes,
an app PR. Questions or recommendations alone do not authorize publication. Honor local-only limits;
if those prevent a required upstream PR, report it as pending rather than claiming full completion.

## Resolve the target and owners

- Read `skill://brew-clear`, `skill://brian-voice`, the target renderer's `AUTHORING.md` and applicable
  personal runtime guidance. Use `skill://brew-test` for UI testing guides. Resolve the existing page,
  slug, source, assets and current renderer; do not create a competing page or use a stale bundle.
- Distinguish page content, shared renderer/UI behavior, authoring skills and machine/runtime setup.
  Brian's `grounds-personal` owns his personal Brew app; `skills` owns authoring skills; dotfiles owns
  personal configuration. Verify current checkouts/remotes before editing or copying anything.
  `Kubera-Health/brew-content` is not a personal repo, and its release workflow is not the Kubera
  single-page publication path. Do not put private company/customer content into personal repos.
- Establish the page's actual durable owner. If its preview is outside Git, persist only content
  suitable for the verified destination; never create a repo in a scratch preview directory or
  silently choose a public personal repository for private content. An unavailable suitable owner
  blocks that archival step, not independent safe local verification.

## Local first, then durable commits

1. Edit the actual local page/shared source before publishing or opening a PR. Reuse shared styles,
   theme controls and checklist behavior rather than adding page-specific replacements.
2. Build/validate with the owner's documented commands and inspect the rendered page in the current
   local renderer. For shared changes, exercise the affected interaction and an unchanged representative
   page, including relevant theme, narrow-layout, link and checklist behavior. Follow active browser
   rules without stealing focus. Preserve existing preview URLs, asset mounts and saved user progress.
3. After local proof, commit only the requested changes to each owning personal repo and push to
   its verified remote/branch. Keep app code, company content, private data and credentials out of
   personal commits. Report exact blockers instead of treating an untracked preview as durable storage.

## Carry meaningful changes into the app

A meaningful reusable change affects shared rendering, design/theme, navigation, links, checklists,
accessibility, publishing/security behavior or the authoring contract that app users rely on. Size
is not the threshold: a one-line functional fix counts. Ordinary article wording, a ticket-specific
page or a one-off diagram does not by itself require an app code PR.

For a meaningful reusable change, the personal commit alone is not completion:

- Inspect the current app implementation and full relevant diff. Port the equivalent change into
  the app's owned Brew source/docs using its patterns, not a blind copy of the personal app or page.
  Keep personal content, configuration and secrets out of the app diff.
- Follow `skill://execute` and the relevant app implementation/revision, verification and PR rules.
  Reuse the agreed approach; reopen discussion only for a material change. Derive the normal target
  branch from the assignment/repo, not an assumed release or hotfix path. Exercise the app path too;
  personal-renderer proof is not proof of the app implementation.
- Update an existing authorized matching PR or create a scoped draft PR into the app. Use Brian's
  voice, describe the shared behavior and observed verification, and link the personal commit when
  reviewer-accessible and free of private material. Do not merge or deploy. If the app already has
  the equivalent change, cite the current source/merged PR instead of creating an empty duplicate PR.

## Hosted publication is separate

A local preview, personal push or app PR does not publish a hosted Brew page. Keep pages local unless
Brian explicitly requests hosting. For Kubera hosting, read the current app's `AUTHORING.md` and
`docs/engineering/internal-apps-aws.md`, inspect the slug/existing object, and use the app runtime's
`page:publish` CLI with the documented account/profile/bucket. Verify the uploaded version and hosted
page where authentication permits. Do not substitute a content-repo merge, direct S3 upload or app
deployment. A shared runtime change still needs the app PR even if its demonstration page is hosted.

Return the local page URL, personal commit/branch links, required app PR (or exact upstream blocker),
checks actually exercised and hosted status. Never imply a push/PR deployed or published anything.
