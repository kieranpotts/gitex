# mise to pin the development toolchain

- Authors: Kieran Potts [@kieranpotts]
- Created: 2026-10-29
- Decision date: TBD
- PR: TBD

## Status

PROPOSED

## Context

GitEx's development toolchain is Python and Poetry for the test suite, and ShellCheck for linting the shell scripts. Until now, each environment sourced these tools its own way.

- On the host, contributors installed them by hand, against documented minimums (Python >= 3.12, Poetry >= 2.2), and ShellCheck from the distro's package manager.

- In the dev container, the versions were whatever the base image shipped.

- In CI, Poetry was the latest from `pip`, Python came from `actions/setup-python`, and ShellCheck was whatever the runner image had.

So the three environments drift apart. This matters most for ShellCheck, because different versions report different findings. `./run/check` can pass on the host and fail in CI, or the other way round. Poetry drifts too, because each version rewrites the header of `poetry.lock`, which produces noisy diffs.

The minimum Python version was also inconsistent. `pyproject.toml` allowed 3.11, but the docs and `AGENTS.md` said 3.12.

## Decision

We will pin the toolchain in a `mise.toml` file at the project root, and use [mise](https://mise.jdx.dev) to install it in every environment.

```toml
[tools]
python = "3.12"
poetry = "2.5"
shellcheck = "0.11.0"
```

- `./run/install` is the single setup entrypoint for the host, the dev container, and CI. In the dev container it is run by hand, like on the host. It runs `mise trust`, `mise install`, then `mise exec -- poetry install`. If mise is missing, it exits with a message saying where to get it.

- `./run/check` and `./run/fix` invoke every tool through `mise exec --`, so they use the pinned versions whether or not mise is activated in the calling shell.

- CI installs mise with `jdx/mise-action`, pinned to a commit SHA per TS-60, then runs `./run/install` like any other environment.

- The minimum Python version in `pyproject.toml` goes up to `^3.12`, and Ruff's `target-version` to `py312`, to match the pin.

- Ruff stays a Poetry dev dependency, locked in `poetry.lock`, and not in `mise.toml`.

mise is a development dependency only. The `bin/` scripts ship as plain POSIX shell, and GitEx users never need mise.

## Consequences

The host, the dev container, and CI run the same tool versions. A version bump is a one-line change to `mise.toml`, followed by `./run/install`.

mise becomes a hard prerequisite for contributing outside the dev container.

`./run/install` trusts `mise.toml` on the contributor's behalf. Running the script is already a decision to trust the repository, but it means a change to `mise.toml` that adds hooks, tasks, or environment variables takes effect without a separate `mise trust` prompt.

The mise version is not pinned in `mise.toml`, because mise can't pin itself. CI pins it in the `version` input in `.github/workflows/integration.yaml`. The dev container gets mise from the `kieranpotts/devcontainer` base image, at whichever version that image's release installs. The two can differ, but `mise.toml` pins the tools themselves, so this matters only if a `mise.toml` feature needs a newer mise.

Python and Poetry are pinned to a minor version, so patch releases still drift. Only ShellCheck is pinned exactly, because its findings change between releases.

CI no longer uses `setup-python`'s Poetry cache, so the `test` job can take a little longer.

## Alternatives

**Keep documented minimums.** This takes no new tooling, but it is exactly the drift described above.

**Rely on the dev container alone.** This pins the tools inside the container, but does nothing for CI or for contributors who work on the host.

**asdf.** It uses the same model, but mise is a single fast binary, it installs Poetry and ShellCheck from its own registry without extra plugins, and the `kieranpotts/devcontainer` base image has adopted it anyway.

**Nix or Devbox.** These give stronger reproducibility, but they are much heavier and harder to learn than a three-tool shell project needs.

**A separate mechanism per tool** (pyenv, pipx, and apt pins). That means three version sources to keep in sync, each installed differently on each platform.

## References

- [`mise.toml`](../../../mise.toml)
- [`run/install`](../../../run/install)
- [mise documentation](https://mise.jdx.dev/configuration.html)
- [`jdx/mise-action`](https://github.com/jdx/mise-action)
- [TS-60](https://kieranpotts.com/standards/060)
