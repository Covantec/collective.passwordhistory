import logging

from zope.component import adapter, getUtility
from Products.PluggableAuthService.interfaces.events import \
        IPrincipalDeletedEvent

from collective.passwordhistory.interfaces import IUsedPasswordStorage

log = logging.getLogger('collective.passwordhistory')

@adapter(IPrincipalDeletedEvent)
def clearPasswordsHandler(event):
    login = event.principal.getUserName()
    storage = getUtility(IUsedPasswordStorage)
    storage.clearPasswordsForUser(login)
    log.info('Password history for user %s deleted' % login)
