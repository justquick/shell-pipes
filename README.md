# Python Shell Pipes

### A simple way to access your shell commands in Python and use them as pipes

The `shpipes` package uses `subprocess.Popen` to run commands in a shell easily from native Python.

```python
    >>> from shpipes import Pipe
    # python --version
    >>> Pipe('python')('--version').getvalue()
    'Python 3.8.6\n'
```

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

Shell Pipes can also collect all executables from your `PATH` variable and gather them into a `Commands` instance so you can use the lib just like your native shell.

```python
    >>> from shpipes import Commands
    >>> shell = Commands()
    # find . -type f | grep .py$ | wc
    >>> shell.find('.', '-type', 'f') | shell.grep('.py$') | shell.wc()
    '      9       9     162\n'
    # this also works
    >>> pipe = shell.find('.', '-type', 'f')
    >>> pipe |= shell.grep('.py$')
    >>> pipe |= shell.wc()
    >>> pipe.getvalue()
    '      9       9     162\n'
```
