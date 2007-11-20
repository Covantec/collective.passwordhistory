import unittest

from zope.testing.doctestunit import DocFileSuite

from zope.component.testing import tearDown

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from zope.testing import doctest

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.NORMALIZE_WHITESPACE |
	       doctest.ELLIPSIS)

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import collective.passwordhistory
    zcml.load_config('configure.zcml', collective.passwordhistory)
    fiveconfigure.debug_mode = False

    ztc.installPackage('collective.passwordhistory')

setup_product()
ptc.setupPloneSite(products=['collective.passwordhistory'])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests((
        DocFileSuite(
	    'storage.txt',
	    tearDown=tearDown,
	    optionflags=OPTIONFLAGS,
        ),
        ztc.ZopeDocFileSuite(
	    'README.txt',
	    package='collective.passwordhistory',
	    test_class=ptc.FunctionalTestCase,
	    optionflags=OPTIONFLAGS,
	),
    ))
    return suite
