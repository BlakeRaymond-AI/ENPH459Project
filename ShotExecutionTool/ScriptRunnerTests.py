__author__ = 'Blake'

import os
import os.path
import unittest
from ScriptRunner import ScriptRunner


class ScriptRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tempFile = 'foo.tmp'
        with open(self.tempFile, 'w') as _:
            pass

    def tearDown(self):
        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)

    def test_loadFromFile(self):
        with open(self.tempFile, 'w') as f:
            f.write('foo')
        runner = ScriptRunner(self.tempFile)
        self.assertEqual(self.tempFile, runner.scriptPath)

    def test_executeCapturesStdout(self):
        script = "print 'Foobar'"
        with open(self.tempFile, 'w') as f:
            f.write(script)
        runner = ScriptRunner(self.tempFile)
        out, _ = runner.execute()
        self.assertEqual('Foobar\n', out)

    def test_executeCapturesStderr(self):
        script = "raise Exception('foo')"
        with open(self.tempFile, 'w') as f:
            f.write(script)
        runner = ScriptRunner(self.tempFile)
        _, err = runner.execute()
        self.assertTrue('Exception: foo' in err)

    def test_canExecuteAsync(self):
        script = "print 'Foobar'"
        with open(self.tempFile, 'w') as f:
            f.write(script)
        runner = ScriptRunner(self.tempFile)
        runner.executeAsync()
        out, _ = runner.join()
        self.assertEqual('Foobar\n', out)


if __name__ == '__main__':
    unittest.main()
