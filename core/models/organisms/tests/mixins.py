from __future__ import unicode_literals, absolute_import, print_function, division

from django.test import TestCase


class TestProcessorMixin(TestCase):

    def test_hooks(self):
        self.skipTest("not tested")
        #process, method = self.new.prepare_process(self.new.process)
        #self.assertIsInstance(process, HttpResourceProcessor)
        #self.assertTrue(callable(method))