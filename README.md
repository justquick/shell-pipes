# Python Shell Pipes

### A simple way to access your shell commands in Python

The `shpipes` package uses `subprocess.Popen` to run commands in a shell easily from native Python.

```python
    >>> from shpipes import Pipe
    # python --version
    >>> Pipe('python')('--version').getvalue()
    'Python 3.8.6\n'
```

## Chaining pipes together

You can chain together your commands, passing output from one to the input of another, similar to shell pipes. You can use the bitwise inclusive or operator to chain `Pipe` instances together.

```python
    # echo 1+1 | bc
    >>> (Pipe('echo')('1+1') | Pipe('bc')).getvalue()
    '2\n'
    # This also works
    >>> pipe = Pipe('echo')('1+1')
    >>> pipe |= Pipe('bc'))
    >>> pipe.getvalue()
    '2\n'
```

### Loading commands from your `PATH`

Shell Pipes can also collect all executables from your `PATH` variable and gather them into a `Commands` instance so you can use the lib just like your native shell.

```python
    >>> from shpipes import Commands
    >>> shell = Commands()
    # find . -type f | grep .py$ | wc -l
    >>> (shell.find('.', '-type', 'f') | shell.grep('.py$') | shell.wc('-l')).getvalue()
    '9\n'
    # this also works
    >>> pipe = shell.find('.', '-type', 'f')
    >>> pipe |= shell.grep('.py$')
    >>> pipe |= shell.wc('-l')
    >>> pipe.getvalue()
    '9\n'
```


### Handling pipe arguments

When a `Pipe` is called, its arguments are directly passed to `Popen` so beware that strings must be quoted properly.
You can use `getvalue()` to get the output from one pipe and then pass it as a command argument instead of input text.
Pipes are only evaluated when `getvalue()` is called

```python
    >>> license = shell.find('.', '-name', '"LICENSE"').getvalue()
    >>> shell.wc(license).getvalue()
    '  21  169 1069 ./LICENSE\n'
```

## Shell by default

Since pipes run in a shell by default, environment variables evaluate automatically

```python

    >>> pipe = shell.ps('-u $USER')
    >>> pipe |= shell.grep('python')
    >>> pipe |= shell.head('-1')
```

### Configuration options

If you need to run a different shell or disable shell entirely, then you can pass options via environment variables or kwargs to `Pipe`


### Overriding options in `Pipe`

You can override all options to `Popen` (except `stdin`/`stdout`) by passing arguments to `Pipe`
By default `Popen` is run in shell mode with your default shell.

```python
    >>> Pipe('ls', executable='/bin/zsh', cwd='/var', shell=False)
```

### Set env `SHPIPES_NO_SHELL`=true

Sets `shell=False` in the call to `Popen`

### Set env `SHPIPES_SHELL`=/bin/zsh

Changes the executable shell run by `Popen`
