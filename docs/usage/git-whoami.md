# `git whoami`

Display the currently configured Git user identity.

This command shows the user name and email address that will be used for commits in the current repository. It checks both local repository configuration and global configuration, with local settings taking precedence.

If either the name or email is not configured, `[not set]` is displayed for that field. This helps identify configuration issues before making commits.

## Usage

```
$ git whoami
```

This command does not accept any arguments.

## Examples

When both name and email are set:

```
$ git whoami
name:  Kieran Potts
email: kieranpotts@users.noreply.github.com
```

When user identity is not configured:

```
$ git whoami
name:  [not set]
email: [not set]
```

Or when the user identity is partially configured:

```
$ git whoami
name:  John Doe
email: [not set]
```

This indicates you need to configure your identity before making commits:

```
$ git config user.name "Your Name"
$ git config user.email "your.email@example.com"
```

### Local vs global configuration

Local repository configuration overrides global settings. To check which configuration is being used:

```
$ git config --global user.name
Alice Smith

$ git config --local user.name
Bob Jones

$ git whoami
name:  Bob Jones
email: alice@example.com
```

In this example, the `user.name` configured for the local repository (Bob Jones) takes precedence over the global configuration (Alice Smith).

## See also

- [`git author`](./git-author.md): Show commit authorship information.
