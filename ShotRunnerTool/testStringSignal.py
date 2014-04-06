import unittest
from PyQt4.QtCore import QString
from ShotRunnerTool.StringSignal import StringSignal


class TestStringSignal(unittest.TestCase):
    received = False

    def test_canEmitStringSignals(self):
        self.received = False
        sentMessage = 'Foobar'

        def receive(s):
            self.assertIsInstance(s, QString)
            self.assertEqual(sentMessage, s)
            self.received = True

        signal = StringSignal()
        signal.get().connect(receive)
        signal.get().emit(sentMessage)
        self.assertTrue(self.received)

    def test_differentInstancesAreIndependent(self):
        messages1 = []
        messages2 = []

        def receive1(s):
            messages1.append(str(s))

        def receive2(s):
            messages2.append(str(s))

        signal1 = StringSignal()
        signal2 = StringSignal()
        signal1.get().connect(receive1)
        signal2.get().connect(receive2)

        signal1.get().emit('')
        self.assertEqual(1, len(messages1))
        self.assertEqual(0, len(messages2))
        signal2.get().emit('')
        self.assertEqual(1, len(messages1))
        self.assertEqual(1, len(messages2))
