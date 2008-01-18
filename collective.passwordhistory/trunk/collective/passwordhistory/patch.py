import logging

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.RegistrationTool import RegistrationTool
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin

log = logging.getLogger('collective.passwordhistory')

def testPasswordValidity(self, password, confirm=None, userid=None):
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

    if not userid:
        membership_tool = getToolByName(self, 'portal_membership')
        userid = membership_tool.getAuthenticatedMember().getId()

    for validator_id, validator in validators:
        set_id = ''
        set_info = {'password':password}
        errors = validator.validateUserInfo( userid, set_id, set_info )
        err += [info['error'] for info in errors if info['id'] == 'password' ]
    if err:
        return ' '.join(err)
    else:
        return None

RegistrationTool.testPasswordValidity = testPasswordValidity
log.info('Patching RegistrationTool.testPasswordValidity to use PAS validation plugins')

