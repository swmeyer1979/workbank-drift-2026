# GitHub identity attribution fix spec

Date: 2026-07-07
Scope: S

## Objective

Use Sam's GitHub identity for `swmeyer1979` on repo commits.

## Files

- `specs/2026-07-07-github-identity-attribution-fix.md`
- Local repo git config
- Git commit metadata on `master`

## Acceptance Criteria

- Local repo git config uses `Sam Meyer <96443875+swmeyer1979@users.noreply.github.com>`.
- Every commit on `master` links to GitHub login `swmeyer1979`.
- `origin/master` points at local `HEAD`.
- No `CEO Agent` or `ceo@paperclip.local` remains on the branch path.

## Risks

- Rewriting pushed history changes commit hashes. Use `git push --force-with-lease`.
- Private email exposure. Use GitHub verified noreply address.
