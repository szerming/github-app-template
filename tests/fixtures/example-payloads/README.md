# Vendored: GitHub's published example payloads

`api.github.com/` — every file the pinned revision of Octokit's example set
carries, laid out exactly as upstream has it: one file per event+action (with the
variants GitHub publishes, such as `created.with-organization`), under a directory
named after the event header.

    repository  octokit/webhooks
    revision    049c104cd2198f5c04acf4ee806b56d2d8fd1e76
    path        payload-examples/api.github.com
    licence     MIT
    273 example payloads across 60 event types

Vendor (or re-vendor) them with:

    base=https://raw.githubusercontent.com/octokit/webhooks/049c104cd2198f5c04acf4ee806b56d2d8fd1e76
    gh api "repos/octokit/webhooks/git/trees/049c104cd2198f5c04acf4ee806b56d2d8fd1e76?recursive=1" \
      --paginate --jq '.tree[] | select(.path|startswith("payload-examples/api.github.com/")) | select(.type=="blob") | .path' \
    | while read -r path; do
        rel="${path#payload-examples/api.github.com/}"
        mkdir -p "$(dirname "api.github.com/$rel")"
        curl -sSf -o "api.github.com/$rel" "$base/$path"
      done

They are held here so that the tests asserting what the models cover need no
network (spec 0001, user story 43). `MANIFEST.json` records the sha256 of every
file as committed, and the tests recompute it, so an edited fixture fails rather
than quietly changing what the models are said to cover. The event type is the
directory and the action is what the payload carries, so nothing is kept in a
table beside them.
