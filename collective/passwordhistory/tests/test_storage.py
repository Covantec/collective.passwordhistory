import unittest
import doctest
import zope.testing

from collective.passwordhistory import storage

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        zope.testing.doctest.DocFileSuite(
            'storage.txt',
            package='collective.passwordhistory',
	    optionflags=optionflags,
	)
    )
    return suite
