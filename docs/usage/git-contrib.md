# `git contrib`

List all contributors to a repository, ordered by their total commit count.

This command provides a summary view of all contributors who have made commits to the repository. Each contributor is listed with their name, email address, and the total number of commits they have authored. Contributors are sorted in descending order by commit count, showing the most active contributors first.

The command analyzes the entire commit history accessible from HEAD. If the repository has no commits yet, no output is produced.

## Usage

```
$ git contrib
```

This command does not accept any arguments.

## Examples

```
$ git contrib
     3	Jane Smith <jane.smith@example.com>
     2	Bob Johnson <bob@example.com>
     1	Alice Wong <alice@example.com>
```

In this example, Jane Smith is the most active contributor with 3 commits, followed by Bob Johnson with 2 commits, and Alice Wong with 1 commit.

## See also

- [`git author`](./git-author.md): Change the author of a commit.
- [`git whoami`](./git-whoami.md): Display your currently configured Git user identity.
