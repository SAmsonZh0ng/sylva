# Sylva

First published release of Sylva, an EE1111A automatic plant-care product concept.

**Live site: https://samsonzh0ng.github.io/sylva/**

GitHub Pages deploys automatically from `main`. The workflow assembles `dist/`
and verifies every public file against `.release/verify.json` before publishing.

Some first-release files are stored in a split archive in `.release/` because
the original upload connection timed out on ordinary Git transfers. The archive
contains only the remaining static website files and is unpacked during deployment.

For future releases, update the complete website and its release manifest/archive
together. The working source remains in the local Sylva project; the initial full
source snapshot is retained locally on branch `release-v1-snapshot`.

Asset credits and library license notices are included with the public assets.
Course files, working scenes, internal documentation and draft films stay local.
