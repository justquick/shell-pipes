import subprocess
import os

OPTIONS = {
    'stdout': subprocess.PIPE,
    'shell': False if 'PIPES_NO_SHELL' in os.environ else True,
    'executable': os.environ.get('PIPES_SHELL', '/bin/bash')
}


class Pipe:
    """
    Pipe class to handle execution of command
    Init sets the command to execute
    Call returns self with the arguments setup
    Run executes the command with any previous Pipe instances
    """
    cmd = None
    args = None
    chain = []

    def __init__(self, cmd, **options):
        self.cmd = cmd
        self.options = OPTIONS.copy()
        self.options.update(options)

    def __call__(self, *args):
        argstr = ''
        for arg in args:
            if isinstance(arg, Pipe):
                argstr += arg.getvalue()
            else:
                argstr += str(arg)
            argstr += ' '
        self.args = argstr.strip()
        return self

    def run(self, inp=None):
        args = self.cmd
        if self.args:
            args += ' ' + self.args
        if inp:
            kwargs = self.options.copy()
            kwargs['stdin'] = inp.stdout
            return subprocess.Popen(args, **kwargs)
        return subprocess.Popen(args, **OPTIONS)

    def getchain(self):
        return self.chain[:] + [self]

    def getvalue(self):
        chain = self.getchain()
        inp = chain[0].run()
        for link in chain[1:]:
            inp = link.run(inp)
        value = inp.stdout.read()
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return value

    def __or__(self, other):
        other.chain.append(self)
        return other

    def __repr__(self):
        if self.args:
            return '<Pipe:"{} {}">'.format(self.cmd, self.args)
        return '<Pipe:{}>'.format(self.cmd)


class Commands:
    """
    Builtin command container. Gathers executables from PATH
    """

    def __init__(self):
        for path in os.environ['PATH'].split(os.pathsep):
            path = os.path.realpath(path)
            if os.path.isdir(path):
                for fname in os.listdir(path):
                    fpath = os.path.realpath(os.path.join(path, fname))
                    if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
                        setattr(self, fname.replace('.', '_').replace('-', '_'), Pipe(fpath))
