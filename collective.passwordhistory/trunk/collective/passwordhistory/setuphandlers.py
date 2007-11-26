from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from collective.passwordhistory.config import PLUGIN_NAME

def importVarious(context):
    if context.readDataFile('collective.passwordhistory_various.txt') is None:
        return
  
    portal = context.getSite()
    setupPlugin(portal)

def setupPlugin(portal):
    """Install and prioritize the password history PAS plug-in
    """
    out = StringIO()

    uf = getToolByName(portal, 'acl_users')

    passwordhistory = uf.manage_addProduct['collective.passwordhistory']
    existing = uf.objectIds()

    if PLUGIN_NAME not in existing:
        passwordhistory.manage_addPasswordHistory(PLUGIN_NAME)
        activatePluginInterfaces(portal, PLUGIN_NAME, out)
	uf.plugins.movePluginsUp(IUserAdderPlugin, [PLUGIN_NAME])
	uf.plugins.movePluginsUp(IUserManagement, [PLUGIN_NAME])
    else:
        print >> out, "%s already installed" % PLUGIN_NAME

    return out.getvalue()
