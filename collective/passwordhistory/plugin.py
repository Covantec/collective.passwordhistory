import logging

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from zope.interface import implements
from zope.component import getUtility

from zope.app.component.hooks import getSite

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin

from Products.PlonePAS.interfaces.plugins import IUserManagement

from collective.passwordhistory.interfaces import IUsedPasswordStorage

log = logging.getLogger('collective.passwordhistory')

manage_addPasswordHistoryForm = PageTemplateFile(
        "zmi/PasswordHistoryForm.pt", globals(),
        __name__="manage_addPasswordHistoryForm")

def manage_addPasswordHistory(dispatcher, id, title=None, REQUEST=None):
    """Add a PasswordHistory plugin to a Pluggable Auth Service."""
    ph = PasswordHistory(id, title)
    dispatcher._setObject(ph.getId(), ph)

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(
                '%s/manage_workspace?manage_tabs_message=PasswordHistory+plugin+added.'
                % dispatcher.absolute_url())


class PasswordHistory(BasePlugin):

    """PAS plugin that keeps a history of previously used passwords
    """

    meta_type = 'Password History'
    security = ClassSecurityInfo()

    _properties = ( { 'id'    : 'title'
                    , 'label' : 'Title'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'history_size'
                    , 'label' : 'History Size'
                    , 'type'  : 'int'
                    , 'mode'  : 'w'
                    }
		  )

    def __init__(self, id, title=None, history_size=3):
        self._id = self.id = id
        self.title = title
        
	self.history_size = history_size
        self._storage = getUtility(IUsedPasswordStorage)

    #
    # IValidationPlugin implementation
    #

    security.declarePrivate('validateUserInfo')
    def validateUserInfo(self, userid, set_id, set_info):
        """ Check if password has been used previously by this user.
        """
        errors = []

        if set_info and set_info.get('password', None):
	    password = set_info['password']

            pas = self._getPAS()
            user = pas.getUserById(userid)
            if user is not None:
                login = user.getUserName()

                if self._storage.isPasswordUsed(login, password, self.history_size):
	            error_msg = "You have used this password before, " \
		                "please use a different password."
	            errors = [{'id':'password','error':error_msg}]

        return errors

    #
    # IUserManagement implementation
    #

    security.declarePrivate('doAddUser')
    def doAddUser(self, login, password):
        """
	Add a user record to a User Manager, with the given login and password

        o Return a Boolean indicating whether a user was added or not
        """
        site = getSite()
        if not site.validate_email:
            self._storage.setPasswordForUser(login, password)
	return False

    security.declarePrivate('doChangeUser')
    def doChangeUser(self, login, password, **kw):
        """
        Change a user's password (differs from role) roles are set in
        the pas engine api for the same but are set via a role
        manager)
        """
	self._storage.setPasswordForUser(login, password)
	return False

    security.declarePrivate('doDeleteUser')
    def doDeleteUser(self, login):
        """
        Remove a user record from a User Manager, with the given login
        and password

        o Return a Boolean indicating whether a user was removed or not
        """
        self._storage.clearPasswordsForUser(login)
	return False

classImplements(PasswordHistory, IValidationPlugin, IUserManagement)
InitializeClass(PasswordHistory)
