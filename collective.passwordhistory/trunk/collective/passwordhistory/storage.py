from zope.interface import implements

from persistent import Persistent
from BTrees.OOBTree import OOBTree
from AccessControl import AuthEncoding

from collective.passwordhistory.interfaces import IUsedPasswordStorage

class UsedPasswordStorage(Persistent):
    """A local utility for storing a list of previously used passwords.
    """

    implements(IUsedPasswordStorage)

    def __init__(self):
        self._user_passwords = OOBTree()

    def isPasswordUsed(self, login, password, history_size=0):
        """Query password store to see if password has been previously used.
        """
	for hash in self.getPasswordsForUser(login, history_size):
	    if AuthEncoding.pw_validate(hash, password):
	        return True
        return False

    def getPasswordsForUser(self, login, history_size=0):
        """Return a list of previously used paswords for a user.
        """
	hashes = self._user_passwords.get(login, [])[-history_size:]
	return hashes

    def setPasswordForUser(self, login, password):
        """Add password to the list of previously used passwords for a user.
        """
	hashes = self._user_passwords.get(login, [])
        hash = AuthEncoding.pw_encrypt(password)
        hashes.append(hash)
        self._user_passwords[login] = hashes

    def clearPasswordsForUser(self, login):
        """Remove stored passwords for a user.
        """
        del self._user_passwords[login]

    def clearAllPasswords(self):
        """Remove stored passwords for all users.
        """
	self._user_passwords.clear()
