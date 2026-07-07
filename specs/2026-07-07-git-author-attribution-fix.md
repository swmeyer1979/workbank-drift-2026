# Git author attribution fix spec

Date: 2026-07-07
Scope: S

## Objective

Rewrite recent repo commits so GitHub shows Sam Meyer as author and committer.

## Files

- `specs/2026-07-07-git-author-attribution-fix.md`
- Git commit metadata for commits authored as `CEO Agent <ceo@paperclip.local>`
- Local repo git config for future commits in this repo

## Acceptance Criteria

- Local repo git config uses `Sam Meyer`.
- Commits `64ceccd` and `c2fb577` no longer have `CEO Agent` author or committer metadata on `master`.
- `git log` shows Sam Meyer for rewritten commits.
- `origin/master` points at the rewritten local `HEAD`.
- Posting files still name Sam Meyer.

## Risks

- Rewriting pushed history changes commit hashes. Use `git push --force-with-lease`.
- Wrong email may fail GitHub account association. Use the same Sam email already present in earlier repo commits.
