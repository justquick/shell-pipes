# encoding: utf-8
import sys
import os
import unittest
import inspect

test_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(test_dir, '..')))


class PipesTest(unittest.TestCase):

    def setUp(self):
        from shpipes import Commands

        os.environ['PATH'] = os.path.join(test_dir, 'bin') + ':' + os.environ['PATH']
        self.shell = Commands()

    def test_path(self):
        attrs = dir(self.shell)
        self.assertIn('wc_py', attrs)
        self.assertIn('eval_py', attrs)
        self.assertIn('grep_py', attrs)
        self.assertIn('massedit_py', attrs)
        self.assertNotIn('noexecfile', attrs)

    def test_math(self):
        echo = self.shell.echo_py('1+3*4')
        cmd = echo | self.shell.eval_py()
        self.assertEqual('13\n', cmd.getvalue())
        cmd = echo | self.shell.eval_py() | self.shell.wc_py()
        self.assertEqual('1\t1\t3\n', cmd.getvalue())

    def test_python(self):
        from shpipes import Pipe

        py_pipe = Pipe(sys.executable)
        cmd = py_pipe('-c "import sys; print(sys.executable)"')
        self.assertEqual(sys.executable + '\n', cmd.getvalue())
        cmd = py_pipe(sys.executable)('--version')
        version = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
        self.assertIn(version, cmd.getvalue())

    def test_grep(self):
        cmd = self.shell.grep_py('.+foobarbaz', __file__)
        self.assertEqual(inspect.stack(2)[0].code_context[0], cmd.getvalue())

    def test_args(self):
        cmd = self.shell.echo_py('4**4')
        cmd = self.shell.eval_py(cmd.getvalue())
        self.assertEqual('256\n', cmd.getvalue())
        cmd = self.shell.eval_py(self.shell.echo_py('4**4'))
        self.assertEqual('256\n', cmd.getvalue())

    def test_bin(self):
        cmd = self.shell.echo_py('"\xff\xff"')
        self.assertEqual('ÿÿ\n', cmd.getvalue())


if __name__ == '__main__':
    unittest.main()
    # self.shell.massedit_py('-e', '''re.sub(r"^class", "classy", line)''')

#
# cmd = cmds.find('. -type f')
# cmd |= cmds.grep(__file__)
# print(cmds.wc(cmd).getvalue())
#
# print(cmd.getvalue())
#
# cmd = cmds.echo("750/12.5") | cmds.bc() | cmds.sed("'s/$/\/24/'") | cmds.bc()
# print(cmd.getvalue())
#
# cmd = Pipe(sys.executable)('-c "import sys; print(sys.version)"')
# print(cmd.getvalue())
#
# cmd = cmds.grep('fizzbuzz', __file__)
# print('G', cmd.getvalue())
#
# cmd = cmds.ps('-u $USER -f')
# cmd |= cmds.grep(__file__)
# cmd |= cmds.head('-1')
# print(cmd.getvalue())
