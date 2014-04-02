__author__ = 'Blake'

import unittest

from PyQt4.QtCore import QString

from StringSignal import StringSignal


class testStringSignal(unittest.TestCase):

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
        self.messages1 = []
        self.messages2 = []

        def receive1(s):
            self.messages1.append(str(s))

        def receive2(s):
            self.messages2.append(str(s))

        signal1 = StringSignal()
        signal2 = StringSignal()
        signal1.get().connect(receive1)
        signal2.get().connect(receive2)

        signal1.get().emit('')
        self.assertEqual(1, len(self.messages1))
        self.assertEqual(0, len(self.messages2))
        signal2.get().emit('')
        self.assertEqual(1, len(self.messages1))
        self.assertEqual(1, len(self.messages2))


if __name__ == '__main__':
    unittest.main()
