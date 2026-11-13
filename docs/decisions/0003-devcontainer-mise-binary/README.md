# Checksum-verified mise binary in the dev container

- Authors: Kieran Potts [@kieranpotts]
- Created: 2026-10-29
- Decision date: 2026-10-30
- PR: TBD

## Status

REJECTED

Overtaken by events before it was accepted. The `kieranpotts/devcontainer` base image now installs mise itself (1.10.0), with mise's shims and `~/.local/bin` on `PATH` for every process. This repository's own devcontainer has also been removed, in favor of the one devcontainer for the whole personal workspace, which is built on that base image. So there is no Dockerfile here for the stopgap to live in, and nothing for it to bridge.

## Context

[ADR 0002](../0002-mise-toolchain/README.md) makes mise the source of the toolchain in every environment, including the dev container. The base image, `kieranpotts/devcontainer`, will install mise through its bootstrap only from the release after 1.7.0. Until then, this project's Dockerfile has to install mise itself.

mise's tools must also be on `PATH` for every process in the container, not only for interactive shells. `mise activate` in `~/.bashrc` is read only by interactive Bash, so `docker exec`, editor tasks, Git hooks, and coding agents would not find the tools. The same applies to Poetry, which the base image installs in `~/.local/bin`.

## Decision

We will download the mise release binary for a pinned version, verify it against its published SHA-256 checksum, and install it to `/usr/local/bin`.

- `MISE_VERSION` and one checksum per architecture (`x64`, `arm64`) are build arguments, copied from the release's `SHASUMS256.txt`.

- The build fails on a checksum mismatch, or on any other architecture.

- The install runs as `root`, then the Dockerfile switches back to the `code` user.

- `ENV PATH` prepends mise's shims directory and `~/.local/bin`, so the pinned tools resolve in every process, interactive or not.

This is a stopgap. Once the base image includes mise, everything after the `FROM` and `ENV DEBIAN_FRONTEND` lines is deleted.

## Consequences

A tampered or truncated download fails the build, instead of ending up in the image.

Upgrading mise means bumping three build arguments, plus the matching `version` in the CI workflow (see ADR 0002).

Calls through shims are slightly slower than calls in an activated shell, but they work everywhere without depending on the shell.

The image is built `FROM kieranpotts/devcontainer:latest`, so it will pick up the base image's own mise silently, as soon as that is released. Until this stopgap is removed, the image then holds two copies of mise, and whichever comes first on `PATH` wins. Removing the stopgap is a manual follow-up.

## Alternatives

**The `curl https://mise.run | sh` installer.** It is simpler, but it runs an unpinned, unverified script at build time.

**mise's apt repository.** It adds a third-party apt source and signing key to the image, and pinning a version through apt is less direct than downloading a named release.

**Wait for the base image.** This would block ADR 0002 on an unrelated release.

**`mise activate` in `~/.bashrc`.** It only works in interactive Bash shells, as described above.

## References

- `.devcontainer/Dockerfile`, since removed
- [mise releases](https://github.com/jdx/mise/releases)
