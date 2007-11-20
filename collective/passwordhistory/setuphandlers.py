from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from collective.passwordhistory.config import PASSWORDHISTORY_PLUGIN_NAME

def importVarious(context):

    if context.readDataFile('collective.passwordhistory_various.txt') is None:
        return
  
    portal = context.getSite()
    setup_passwordhistory_plugin(portal)

def setup_passwordhistory_plugin(portal):
    """Install and prioritize the password history PAS plug-in
    """
    out = StringIO()

    uf = getToolByName(portal, 'acl_users')

    passwordhistory = uf.manage_addProduct['collective.passwordhistory']
    existing = uf.objectIds()

    if PASSWORDHISTORY_PLUGIN_NAME not in existing:
        passwordhistory.manage_addPasswordHistory(PASSWORDHISTORY_PLUGIN_NAME)
        activatePluginInterfaces(portal, PASSWORDHISTORY_PLUGIN_NAME, out)
    else:
        print >> out, "%s already installed" % PASSWORDHISTORY_PLUGIN_NAME

    return out.getvalue()
