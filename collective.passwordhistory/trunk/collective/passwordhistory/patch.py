import logging

from AccessControl.Permissions import manage_users as ManageUsers
from AccessControl.requestmethod import postonly

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.RegistrationTool import RegistrationTool
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin

from zope.event import notify
from Products.PluggableAuthService.PluggableAuthService import \
     PluggableAuthService, _SWALLOWABLE_PLUGIN_EXCEPTIONS
from Products.PluggableAuthService.PluggableAuthService import security
from Products.PluggableAuthService.events import PrincipalDeleted

from Products.PlonePAS.interfaces.plugins import IUserManagement

log = logging.getLogger('collective.passwordhistory')

def testPasswordValidity(self, password, confirm=None):
    """ Verify that the password satisfies the portal's requirements.

    o If the password is valid, return None.
    o If not, return a string explaining why.
    """
    if confirm is not None and confirm != password:
        return ( 'Your password and confirmation did not match. '
               + 'Please try again.' )

    if not password:
        err = [ 'You must enter a password.' ]
    else:
        err = []

    # Use PAS to test validity
    pas_instance = self.acl_users
    plugins = pas_instance._getOb('plugins')
    validators = plugins.listPlugins(IValidationPlugin)

    membership_tool = getToolByName(self, 'portal_membership')
    user = membership_tool.getAuthenticatedMember().getId()

    for validator_id, validator in validators:
        #user = None
        set_id = ''
        set_info = {'password':password}
        errors = validator.validateUserInfo( user, set_id, set_info )
        err += [info['error'] for info in errors if info['id'] == 'password' ]
    if err:
        return ' '.join(err)
    else:
        return None
RegistrationTool.testPasswordValidity = testPasswordValidity
log.info('Patching RegistrationTool.testPasswordValidity to use PAS validation plugins')

def _doDelUser(self, id):
    """
    Given a user id, hand off to a deleter plugin if available.
    """
    plugins = self._getOb('plugins')
    userdeleters = plugins.listPlugins(IUserManagement)

    if not userdeleters:
        raise NotImplementedError("There is no plugin that can "
                                  " delete users.")

    for userdeleter_id, userdeleter in userdeleters:
        try:
	    user = self.getUserById(id)
            userdeleter.doDeleteUser(id)
	    notify(PrincipalDeleted(user))
        except _SWALLOWABLE_PLUGIN_EXCEPTIONS:
            pass
PluggableAuthService._doDelUser = _doDelUser

security.declareProtected(ManageUsers, 'userFolderDelUsers')
PluggableAuthService.userFolderDelUsers = postonly(PluggableAuthService._doDelUsers)
