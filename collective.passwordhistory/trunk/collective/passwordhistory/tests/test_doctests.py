import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.Five import zcml
from Products.Five import fiveconfigure

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import collective.passwordhistory
    zcml.load_config('configure.zcml', collective.passwordhistory)
    fiveconfigure.debug_mode = False

    ztc.installPackage('collective.passwordhistory')

setup_product()
ptc.setupPloneSite(products=['collective.passwordhistory'])

from collective.passwordhistory.tests.utils import MockMailHost

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

class MockMailHostTestCase(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = MockMailHost('MailHost')

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        ztc.ZopeDocFileSuite(
	    'README.txt',
	    package='collective.passwordhistory',
            test_class=ptc.PloneTestCase,
            optionflags=optionflags,
	)
    )
    suite.addTest(
        ztc.FunctionalDocFileSuite(
            'plugin.txt',
            package='collective.passwordhistory',
            test_class=MockMailHostTestCase, 
            optionflags=optionflags,
        )
    )
    return suite
