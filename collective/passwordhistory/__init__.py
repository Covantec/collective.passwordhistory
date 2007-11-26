from Products.PluggableAuthService import registerMultiPlugin
from AccessControl.Permissions import add_user_folders

import collective.passwordhistory.patch
from collective.passwordhistory import plugin

registerMultiPlugin(plugin.PasswordHistory.meta_type)

def initialize(context):
    # Register PAS plug-in
    context.registerClass(plugin.PasswordHistory,
                          permission = add_user_folders,
                          constructors = (plugin.manage_addPasswordHistoryForm,
                                          plugin.manage_addPasswordHistory),
                          visibility = None)
