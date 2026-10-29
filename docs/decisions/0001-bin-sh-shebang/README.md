# `#!/bin/sh` shebang for the GitEx scripts

- Authors: Kieran Potts [@kieranpotts]
- Created: 2026-10-27
- Decision date: TBD
- PR: TBD

## Status

PROPOSED

## Context

Every executable script in `bin/` currently starts with the shebang
`#!/bin/env sh`. The scripts in `lib/` use `#!/bin/sh`. The two are
inconsistent, even through they target the same runtime environments.

GitEx's stated targets are Linux, macOS, WSL2, and Git for Windows.

The `run/` scripts use `#!/usr/bin/env bash`. But these are Bash-specific
development helpers, not targetting POSIX shells, and so are not affected by
this decision.

We need to align `bin/` and `lib/` shebangs.

`/bin/env` exists only on Linux distributions where `/bin` is a symlink to
`/usr/bin`, such as Debian 12, Ubuntu, Fedora, and Pop!_OS. On other systems,
`env` is only at `/usr/bin/env`. macOS and FreeBSD also have no `/bin/env`.

POSIX itself guarantees neither `/bin/sh` nor `/usr/bin/env`. It leaves the `#!`
mechanism unspecified, and tells applications to find `sh` with `getconf PATH`.

Git's own shell-script commands, such as `git-filter-branch`, `git-mergetool`,
`git-request-pull`, and `git-subtree`, all use `#!/bin/sh`.

## Decision

We will start every executable script in `bin/` with the following shebang,
consistent with Git's own shell-script commands.

```sh
#!/bin/sh
```

This has the following consequences.

- `bin/` scripts are changed to `#!/bin/sh`.

- `lib/` scripts keep their existing `#!/bin/sh` shebang.

- The script template in the `shell-scripts` skill changes, too.

- `run/` scripts are Bash-only development tools, and so keep their existing
  `#!/usr/bin/env bash`. This shebang is RECOMMENDED for Bash because Bash's
  location varies between systems.

This decision is compatible with [TS-31](https://kieranpotts.com/standards/031),
which recommends `#!/bin/sh` for POSIX scripts and accepts `#!/usr/bin/env sh`
only where a script must run on a legacy system whose `/bin/sh` is not
POSIX-compliant.

Two further reasons are specific to GitEx.

1.  **GitEx commands are Git subcommands.** Git finds and runs `git-<name>`
    scripts in the same way it runs its own shell-script commands, all of which
    use `#!/bin/sh`. Following the same convention means a GitEx command runs
    under the same interpreter as Git's own scripts, on every platform that
    Git supports.

2.  **Several GitEx commands rewrite history or discard work.** For these
    commands, a predictable interpreter matters more than a uniform convention.
    A stray `sh` on the user's `PATH` must not be able to change how
    `git uncommit` behaves.

The one substantive advantage of the env-style shebang is that users can put a
POSIX `sh` earlier on their `PATH`. But that matters only on legacy systems such
as Solaris 10 and earlier, where `/bin/sh` is the pre-POSIX Bourne shell and the
POSIX shell is at `/usr/xpg4/bin/sh`. These systems are not GitEx targets,
anyway.

## Consequences

GitEX scripts now run under whatever the system's `/bin/sh` is, regardless of
the user's `PATH` or interactive shell.

- Dash on Debian, Ubuntu, Pop!_OS, and the default Ubuntu distribution in WSL2.
- Bash in POSIX mode on Fedora, RHEL, Arch, and Git for Windows.
- Bash 3.2 in POSIX mode on macOS.
- BusyBox ash on Alpine.

A user cannot change which interpreter runs GitEx by putting a different `sh`
earlier on their `PATH`. On a system whose `/bin/sh` is not POSIX-compliant,
such as Solaris 10 or earlier, the scripts will not work, and the only
workaround is to invoke them explicitly with a POSIX shell. Such systems are
not GitEx targets, so this cost is accepted.

The pytest helper (`TestRepo.run()` in `test/helper.py`) runs every script as
`bash <script>`. That ignores the shebang and runs Bash in its default,
non-POSIX mode. As a result, a broken shebang cannot cause a test to fail. A
follow-up change should run the scripts as `sh <script>`, or through their
shebang, and add a per-interpreter test matrix.
