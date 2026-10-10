## Agent skills

### Issue tracker

GitHub Issues on `szerming/github-app-template` via the `gh` CLI; specs live in-repo under `docs/specs/`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, label strings unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Local webhook testing

The App's webhook URL is GitHub's, so a delivery reaches the running service only when something forwards it there. Drive live GitHub deliveries at the local service with the `gh webhook` extension (`cli/gh-webhook`, installed):

```
gh webhook forward --repo=szerming/github-app-template --events='*' --secret=<secret> --url=http://localhost:<port>/
```

Take `<secret>` and `<port>` from the start script and the settings it reads — the forwarded signature has to be the one the service verifies with, or every delivery takes the 401 path instead of the accept path.

- Forwarding is live — something must actually happen on the repository, and it needs an authenticated `gh`. It is the demo; the hermetic suite stays the CI gate.
- Omitting `--url` prints each event to stdout instead, the fastest way to see a payload GitHub publishes no example for. `--org=<org>` forwards an organization webhook under the same flags.
- GitHub does not let you approve your own pull request, so a review-approval delivery needs a second account.
