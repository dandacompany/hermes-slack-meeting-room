# Distribution

Recommended order:

1. Local development install.
2. Direct GitHub identifier install.
3. GitHub tap install.
4. Public registry or Hermes optional skill submission after repeated successful installs.

## Local Development

```bash
mkdir -p ~/.hermes/skills/hermes-slack-meeting-room
cp -R skills/hermes-slack-meeting-room/* ~/.hermes/skills/hermes-slack-meeting-room/
hermes skills check
```

## Direct GitHub Identifier Install

After publishing the repo:

```bash
hermes skills install <owner>/<repo>/skills/hermes-slack-meeting-room
```

Use this for early testers because it does not require adding a tap and preserves bundled `assets/`, `references/`, and `scripts/`.

Do not use a raw `SKILL.md` URL for this package. Hermes raw URL installs are single-file installs and cannot discover bundled support files from a bare URL.

## GitHub Tap

Use a GitHub tap when a team will install multiple skills from the same repository.

```bash
hermes skills tap add <owner>/<repo>
hermes skills search "hermes slack meeting"
hermes skills install <identifier-shown-by-search>
```

Expected repo layout:

```text
skills/
  hermes-slack-meeting-room/
    SKILL.md
    assets/
    references/
    scripts/
```

## Publish Command

Hermes can create a GitHub PR for a skill source:

```bash
hermes skills publish ./skills/hermes-slack-meeting-room --to github --repo <owner>/<repo>
```

This requires GitHub authentication through `GITHUB_TOKEN` or `gh auth login`.

ClawHub publishing is currently manual in Hermes CLI:

```bash
hermes skills publish ./skills/hermes-slack-meeting-room --to clawhub
```

The command prints the manual submission URL.
