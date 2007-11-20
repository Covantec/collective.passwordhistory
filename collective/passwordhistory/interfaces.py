from zope.interface import Interface
from zope.interface import Attribute

class IUsedPasswordStorage(Interface):
    """A storage for previously used passwords.
    """

    def isPasswordUsed(userid, password):
        """Query password store to see if password has been previously used.
        """

    def getPasswordsForUser(userid):
        """Return a list of previously used paswords for a user.
	"""

    def setPasswordForUser(userid, password):
        """Add password to the list of previously used passwords for a user.
	"""

    def clearPasswordsForUser(userid):
        """Remove stored passwords for a user.
	"""

    def clearAllPasswords():
        """Remove stored passwords for all users.
	"""
