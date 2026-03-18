# Final Manual Checks

Updated: 2026-03-16

This file contains only the remaining manual checks before arXiv upload or journal submission.

## Remaining Items

1. DOI browser-click verification
2. GitHub tag / release confirmation

## DOI Browser-Click Verification

These two DOI resolvers returned `403` during automated HTTP checks and should be verified once in a normal browser:

- `[4]` `https://doi.org/10.1021/acs.chas.0c00075`
- `[10]` `https://doi.org/10.3390/app12168081`

Expected outcome:
- The DOI opens the correct article landing page.
- The article title matches the manuscript reference entry.

## GitHub Tag / Release Confirmation

This workspace is not a git working tree, so tag/release verification could not be completed locally.

Before submission, confirm:
- the repository URL cited in the paper is correct
- a fixed submission tag or release exists
- the tag/release corresponds to the packaged source snapshot

Recommended release note contents:
- manuscript version date
- exact package filename
- brief statement that the release matches the submission snapshot

## Submission Decision

If the two DOI links resolve correctly in a browser and the GitHub release/tag is fixed, the package is ready for final arXiv upload or initial journal submission.
