import logging

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from zope.component import getUtility
from zope.interface import implements

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import \
    IValidationPlugin, ICredentialsUpdatePlugin

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
    # ICredentialsUpdatePlugin implementation
    #

    security.declarePrivate('updateCredentials')
    def updateCredentials(self, request, response, login, new_password):
        """ Store new password.
	"""
	# Don't remember this password if it's already in the history.
	# This will happen when a user logs in for instance.
	if not self._storage.isPasswordUsed(login, new_password):
	    self._storage.setPasswordForUser(login, new_password)
	    log.info('Password history for user %s updated' % login)

classImplements(PasswordHistory, IValidationPlugin, ICredentialsUpdatePlugin)
InitializeClass(PasswordHistory)
