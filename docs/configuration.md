# Configuration

GitEx commands can be configured using environment variables.

## Environment variables

### `GITEX_DEFAULT_REMOTE_NAME`

Specifies the name of the default remote repository for operations that push to or fetch from a remote.

**Default value:** `origin`

**Used by:** `git-br`

**Example:**

```
# Set in your shell configuration file (~/.bashrc, ~/.zshrc, etc.).
export GITEX_DEFAULT_REMOTE_NAME=upstream

# Or set for a single command.
GITEX_DEFAULT_REMOTE_NAME=upstream git br my-feature
```

This is useful when working with repositories that use a different remote naming convention, such as "upstream" instead of "origin", for the default remote repository.
