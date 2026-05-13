# Installation

All the Git aliases are implemented as shell scripts in the `bin` directory.

To install, all you need to do is clone this repository to your computer, then add this repository's `bin` directory to your system's `PATH` environment variable.

You might do this automatically, eg. in your `~/.bashrc` file:

```bash
if [ -d "$HOME/dev/gitex/bin" ] ; then
  PATH="$PATH:$HOME/dev/gitex/bin"
fi
```

Your user MUST have executable permissions on the shell scripts. You can set this up by running the following command in your terminal, from the root directory of this repository:

```bash
chmod -R u+x bin
```
